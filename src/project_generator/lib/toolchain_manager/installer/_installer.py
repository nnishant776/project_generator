'''
Module for installing the configured toolchains for the project
'''

from dataclasses import dataclass
from copy import deepcopy
import os
import tarfile
import shutil
import subprocess

from typing_extensions import Self

from project_generator.lib.toolchain import Toolchain
from project_generator.lib.distromngr import Distribution
from project_generator.lib.pkgmngr import PackageManagerBuilder
from project_generator.lib.utils.command import CommandBuilder
from ._util import _download_go_toolchain, _download_rust_toolchain


@dataclass(slots=True)
class Installer:
    '''
    Class for exposing operations for installing packages
    '''

    _distribution: Distribution

    def install_toolchain(self) -> int:
        '''
        Install the relevant packages based on the toolchain
        '''


@dataclass(slots=True)
class _CToolchainInstaller(Installer):
    '''
    C Toolchain installer
    '''

    def install_toolchain(self) -> int:
        '''
        C toolchain installer
        '''

        pkg_list = Toolchain.C.packages_for(self._distribution)
        pkg_manager = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(self._distribution) \
            .build()

        return pkg_manager.install(pkg_list).commit()


@dataclass(slots=True)
class _CppToolchainInstaller(Installer):
    '''
    C Toolchain installer
    '''

    def install_toolchain(self) -> int:
        '''
        C++ toolchain installer
        '''

        pkg_list = Toolchain.CPP.packages_for(self._distribution)
        pkg_manager = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(self._distribution) \
            .build()

        return pkg_manager.install(pkg_list).commit()


@dataclass(slots=True)
class _GtkToolchainInstaller(Installer):
    '''
    Gtk Toolchain installer
    '''

    def install_toolchain(self) -> int:
        '''
        Gtk toolchain installer
        '''

        pkg_list = Toolchain.GTK.packages_for(self._distribution)
        pkg_manager = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(self._distribution) \
            .build()

        return pkg_manager.install(pkg_list).commit()


@dataclass(slots=True)
class _GoToolchainInstaller(Installer):
    '''
    Go Toolchain installer
    '''

    def install_toolchain(self) -> int:
        '''
        Go toolchain installer
        '''

        go_tar_file = _download_go_toolchain()

        go_root = os.getenv('GOROOT')
        if go_root is None or go_root == "":
            go_root = "/usr/local/sdks/go"

        extract_path = "/tmp/golang"

        tar_handler = tarfile.TarFile.gzopen(go_tar_file, 'r')
        tar_handler.extractall(extract_path)

        filenames = tar_handler.getnames()

        extracted_path = deepcopy(extract_path)

        common_path = os.path.commonpath(filenames)
        if common_path.startswith(".") is False:
            extracted_path = os.path.join(extracted_path, common_path)

        shutil.rmtree(go_root, True, None)
        os.makedirs(os.path.dirname(go_root), exist_ok=True)
        shutil.move(extracted_path, go_root)

        os.remove(go_tar_file)


@dataclass(slots=True)
class _RustToolchainInstaller(Installer):
    '''
    Rust Toolchain installer
    '''

    def install_toolchain(self) -> int:
        '''
        Rust toolchain installer
        '''

        rustup_init_bin = _download_rust_toolchain()

        os.chmod(rustup_init_bin, 0o755)

        cmd = CommandBuilder().program(rustup_init_bin).option("-y").build()
        ret = cmd.run()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, ' '.join(cmd.flatten()))

        os.remove(rustup_init_bin)


@dataclass(slots=True)
class ToolchainInstallerBuilder:
    '''
    Get the installer based on inputs
    '''
    _distribution: Distribution
    _toolchain: Toolchain

    def __init__(self):
        self._distribution = None
        self._toolchain = None

    def install_toolchain(self, toolchain: Toolchain) -> Self:
        '''
        Specify the toolchain to be installed
        '''
        self._toolchain = toolchain
        return self

    def distribution(self, distribution: Distribution) -> Self:
        '''
        Specify the distribution
        '''
        self._distribution = distribution
        return self

    def build(self) -> Installer:
        '''
        Return the constructed installer
        '''
        if self._toolchain == Toolchain.C:
            return _CToolchainInstaller(self._distribution)
        elif self._toolchain == Toolchain.CPP:
            return _CppToolchainInstaller(self._distribution)
        elif self._toolchain == Toolchain.GTK:
            return _GtkToolchainInstaller(self._distribution)
        elif self._toolchain == Toolchain.GO:
            return _GoToolchainInstaller(self._distribution)
        elif self._toolchain == Toolchain.RUST:
            return _RustToolchainInstaller(self._distribution)
        else:
            return Installer(self._distribution)
