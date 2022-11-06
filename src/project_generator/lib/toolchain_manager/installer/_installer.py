'''
Module for installing the configured toolchains for the project
'''

import os
import shutil
import subprocess
import tarfile
from copy import deepcopy
from dataclasses import dataclass

from typing_extensions import Self

from project_generator.lib.distromngr import Distribution
from project_generator.lib.toolchain import Toolchain
from project_generator.lib.utils.command import CommandBuilder

from ._util import (_download_go_toolchain, _download_rust_toolchain,
                    _install_tools_packages)


@dataclass(slots=True)
class Installer:
    '''
    Class for exposing operations for installing packages
    '''

    _distribution: Distribution

    def install_toolchain(self, path: str = None) -> int:
        '''
        Install the relevant packages based on the toolchain
        '''

    def install_additional_tools(self, path: str = None) -> int:
        '''
        Install common accompanying addtional tools for each toolchain
        '''


@dataclass(slots=True)
class _CToolchainInstaller(Installer):
    '''
    C Toolchain installer
    '''

    def install_toolchain(self, path: str = None) -> int:
        '''
        C toolchain installer
        '''

        pkg_list = Toolchain.C.packages_for(self._distribution)
        return _install_tools_packages(self._distribution, pkg_list)

    def install_additional_tools(self, path: str = None) -> int:
        '''
        C additional tools installer
        '''

        pkg_list = Toolchain.C.extra_packages_for(self._distribution)
        return _install_tools_packages(self._distribution, pkg_list)


@dataclass(slots=True)
class _CppToolchainInstaller(Installer):
    '''
    C++ Toolchain installer
    '''

    def install_toolchain(self, path: str = None) -> int:
        '''
        C++ toolchain installer
        '''

        pkg_list = Toolchain.CPP.packages_for(self._distribution)
        return _install_tools_packages(self._distribution, pkg_list)

    def install_additional_tools(self, path: str = None) -> int:
        '''
        C++ additional tools installer
        '''

        pkg_list = Toolchain.CPP.extra_packages_for(self._distribution)
        return _install_tools_packages(self._distribution, pkg_list)


@dataclass(slots=True)
class _GtkToolchainInstaller(Installer):
    '''
    Gtk Toolchain installer
    '''

    def install_toolchain(self, path: str = None) -> int:
        '''
        Gtk toolchain installer
        '''

        pkg_list = Toolchain.GTK.packages_for(self._distribution)
        return _install_tools_packages(self._distribution, pkg_list)

    def install_additional_tools(self, path: str = None) -> int:
        '''
        Gtk additional tools installer
        '''

        pkg_list = Toolchain.GTK.extra_packages_for(self._distribution)
        return _install_tools_packages(self._distribution, pkg_list)


@dataclass(slots=True)
class _GoToolchainInstaller(Installer):
    '''
    Go Toolchain installer
    '''

    def install_toolchain(self, path: str = None) -> int:
        '''
        Go toolchain installer
        '''

        go_tar_file = _download_go_toolchain()

        go_root: str = None

        if path is not None and path != "":
            go_root = path
        else:
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

    def install_additional_tools(self, path: str = None) -> int:
        '''
        Go additional tools installer
        '''

        go_tools_list = [
            'github.com/cweill/gotests/gotests@latest',
            'github.com/fatih/gomodifytags@latest',
            'github.com/josharian/impl@latest',
            'github.com/haya14busa/goplay/cmd/goplay@latest',
            'github.com/go-delve/delve/cmd/dlv@latest',
            'honnef.co/go/tools/cmd/staticcheck@latest',
            'golang.org/x/tools/gopls@latest',
            'github.com/ramya-rao-a/go-outline@latest'
        ]

        cmd = CommandBuilder() \
            .program('go') \
            .subcommand('install') \
            .args(go_tools_list) \
            .build()

        ret = cmd.run()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, ' '.join(cmd.flatten))


@dataclass(slots=True)
class _RustToolchainInstaller(Installer):
    '''
    Rust Toolchain installer
    '''

    def install_toolchain(self, path: str = None) -> int:
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

    def install_additional_tools(self, path: str = None) -> int:
        '''
        Rust additional tools installer
        '''

        cmd = CommandBuilder() \
            .program('rustup') \
            .subcommand('component') \
            .subcommand('add') \
            .arg('rust-analyzer') \
            .build()

        ret = cmd.run()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, ' '.join(cmd.flatten()))


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
        if self._toolchain == Toolchain.CPP:
            return _CppToolchainInstaller(self._distribution)
        if self._toolchain == Toolchain.GTK:
            return _GtkToolchainInstaller(self._distribution)
        if self._toolchain == Toolchain.GO:
            return _GoToolchainInstaller(self._distribution)
        if self._toolchain == Toolchain.RUST:
            return _RustToolchainInstaller(self._distribution)

        return Installer(self._distribution)
