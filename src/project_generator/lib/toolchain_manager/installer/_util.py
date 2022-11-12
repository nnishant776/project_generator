'''
Utility module used by the installer
'''

import hashlib
import json
import os
import platform
import tempfile

from pathlib import Path
from tarfile import TarError, is_tarfile
from urllib import request
from urllib.error import HTTPError, URLError

from project_generator.lib.distromngr import Distribution
from project_generator.lib.pkgmngr import PackageManagerBuilder
from project_generator.lib.utils.logger import get_logger

lgr = get_logger("installer")


def _check_hash(filename: Path, exp_chksum: str) -> bool:
    '''
    Check if the file with the name "filename" matches the SHA-256 sum in "expect"
    '''
    hash_val = hashlib.sha256()
    with open(filename, 'rb') as f_h:
        while True:
            data = f_h.read(4096)
            if len(data) == 0:
                break
            hash_val.update(data)
    return exp_chksum == hash_val.hexdigest()


class _GoToolchainDownloader:
    '''
    Utility class for managing the download for golang toolchain
    '''

    def __init__(self):
        self._latest_release_info: dict[str, str] = None

    def check_install_file_exists(self, path: Path = None) -> bool:
        '''
        Verify if an already downloaded install file exists
        '''

        try:
            if os.path.exists(path) and os.stat(path).st_size != 0 and is_tarfile(path):
                latest_release_info = self.get_latest_release()
                release_file_info = self.get_latest_release_installer_info(
                    latest_release_info)
                if _check_hash(path, release_file_info.get('sha256')):
                    lgr.debug(
                        "Latest release file found with matching SHA256 hash")
                    return True
                lgr.debug("Latest release found but hash doesn't match")
                return False
            raise FileNotFoundError(
                "No valid golang installation tar file found")
        except (FileNotFoundError, TarError):
            return False

    def get_latest_release(self) -> dict[str, str]:
        '''
        Fetch the latest release information
        '''

        latest_release_info = None

        with request.urlopen("https://go.dev/dl/?mode=json") as resp:
            release_list = json.loads(resp.read())
            latest_release_info = None
            for release in release_list:
                if release.get('stable', False):
                    latest_release_info = release
                    break

        if latest_release_info is None:
            raise ValueError("No stable release found")

        return latest_release_info

    def get_latest_release_installer_info(self, rel_info: dict[str, str]) -> dict[str, str]:
        '''
        Extract the release installer information from the aggregate release info
        '''
        files_info = rel_info.get('files', None)
        if files_info is None:
            raise ValueError(
                f"No files found in the latest release {rel_info.get('version', None)}")

        release_file_info = None
        for file_info in files_info:
            if file_info.get('os', '') == "linux" and file_info.get('arch', "") == "amd64":
                release_file_info = file_info
                break

        if release_file_info is None:
            raise ValueError(
                f"No suitable release binary found in {rel_info.get('version', None)}")

        return release_file_info

    def download_install_tar(self) -> Path:
        '''
        Download the latest released install tar
        '''

        latest_release_info = self.get_latest_release()

        version = latest_release_info.get('version', None)
        if version is None:
            raise ValueError(
                "Version information missing from release info")

        release_file_info = self.get_latest_release_installer_info(
            latest_release_info)

        release_filename = release_file_info.get('filename', None)
        if release_filename is None:
            raise ValueError(
                f"No suitable file found in release {version}")

        release_checksum = release_file_info.get('sha256', None)
        if release_checksum is None:
            lgr.debug("release_info: %s", json.dumps(release_file_info))
            raise ValueError("Checksum info not present in the release info")

        try:
            file_fd, temp_output_path = tempfile.mkstemp()
            # close the return fd, as we are not going to use it
            os.close(file_fd)

            file_dir = os.path.dirname(temp_output_path)
            final_output_path = Path(os.path.join(file_dir, release_filename))

            if self.check_install_file_exists(final_output_path):
                return final_output_path

            lgr.debug("Downloading golang installation tar file from scratch")

            request.urlretrieve(
                f"https://go.dev/dl/{release_filename}", temp_output_path)

            os.rename(temp_output_path, final_output_path)
            temp_output_path = final_output_path

            return temp_output_path

        except (URLError, HTTPError, Exception) as exc:
            os.remove(temp_output_path)
            raise exc


def _download_go_toolchain():
    '''
    Download the Go toolchain
    '''
    go_toolchain_downloader = _GoToolchainDownloader()
    return go_toolchain_downloader.download_install_tar()


def _download_rust_toolchain():
    '''
    Download the Rust toolchain
    '''

    rustup_init_bin = "/tmp/rustup-init"

    target_triple = _get_target_triple()

    request.urlretrieve(
        f"https://static.rust-lang.org/rustup/dist/{target_triple}/rustup-init", rustup_init_bin)

    os.chmod(rustup_init_bin, 0o755)

    return rustup_init_bin


def _get_target_triple() -> str:
    '''
    Generate the target triple for the current system
    '''
    architecture = platform.machine()
    operating_system = platform.system().lower()

    return f"{architecture}-unknown-{operating_system}-gnu"


def _install_tools_packages(distribution: Distribution, pkg_list: list[str]):
    '''
    Helper function to install the packages
    '''

    pkg_manager = PackageManagerBuilder() \
        .confirm_action(False) \
        .distribution(distribution) \
        .build()

    return pkg_manager.install(pkg_list).commit()
