'''
Utility module used by the installer
'''

from urllib import request
import json
import os
import tempfile
import platform


def _download_go_toolchain(temp_output_path=None):
    '''
    Download the Go toolchain
    '''

    try:
        with request.urlopen("https://go.dev/dl/?mode=json") as resp:
            release_list = json.loads(resp.read())
            latest_release = None
            for release in release_list:
                if release.get('stable', False):
                    latest_release = release
                    break

            if latest_release is None:
                raise ValueError("No stable release found")

            version = latest_release.get('version', None)
            if version is None:
                raise ValueError(
                    "Version information missing from release info")

            files_info = latest_release.get('files', None)
            if files_info is None:
                raise ValueError(
                    f"No files found in the latest release {version}")

            release_file = None
            for file_info in files_info:
                if file_info.get('os', '') == "linux" and file_info.get('arch', "") == "amd64":
                    release_file = file_info.get('filename', None)
                    break

            if release_file is None:
                raise ValueError(
                    f"No suitable file found in release {version}")

            # get a valid output path, use temp path if not given
            if temp_output_path is None or temp_output_path == "":
                file_fd, temp_output_path = tempfile.mkstemp()
                # close the return fd, as we are not going to use it
                os.close(file_fd)

            request.urlretrieve(
                f"https://go.dev/dl/{release_file}", temp_output_path)

            file_dir = os.path.dirname(temp_output_path)
            final_output_path = os.path.join(file_dir, release_file)
            os.rename(temp_output_path, final_output_path)
            temp_output_path = final_output_path

    except Exception as exc:
        # clean up the downloaded temporary file in case of failures
        os.remove(temp_output_path)
        raise exc

    return temp_output_path


def _download_rust_toolchain():
    '''
    Download the Rust toolchain
    '''

    rustup_init_bin = "/tmp/rustup-init"

    target_triple = _get_target_triple()

    request.urlretrieve(
        f"https://static.rust-lang.org/rustup/dist/{target_triple}/rustup-init", rustup_init_bin)

    return rustup_init_bin


def _get_target_triple() -> str:
    '''
    Generate the target triple for the current system
    '''
    architecture = platform.machine()
    operating_system = platform.system().lower()

    return f"{architecture}-unknown-{operating_system}-gnu"
