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

        return 0

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

        for tool in go_tools_list:
            cmd = CommandBuilder() \
                .program('go') \
                .arg('install') \
                .arg(tool) \
                .build()

            ret = cmd.run()
            if ret != 0:
                raise subprocess.CalledProcessError(
                    ret, ' '.join(cmd.flatten()))

        return 0


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
class ToolchainInstaller:
    '''
    Installs a given toolchain for the specified distro
    '''

    distribution: Distribution
    toolchain: Toolchain
    install_path: str = ""
    additional_tools: bool = False

    def run(self) -> int:
        '''
        Run the constructed installer
        '''

        if self.toolchain is None or self.toolchain not in Toolchain:
            raise ValueError(
                f"Invalid or unsupported toolchain '{self.toolchain}' specified")

        if self.toolchain not in [Toolchain.GO, Toolchain.RUST] and \
                (self.distribution is None or self.distribution not in Distribution):
            raise ValueError(
                f"Distribution not specified for '{self.toolchain.value}' toolchain")

        installer = None
        if self.toolchain == Toolchain.C:
            installer = _CToolchainInstaller(self.distribution)
        elif self.toolchain == Toolchain.CPP:
            installer = _CppToolchainInstaller(self.distribution)
        elif self.toolchain == Toolchain.GTK:
            installer = _GtkToolchainInstaller(self.distribution)
        elif self.toolchain == Toolchain.GO:
            installer = _GoToolchainInstaller(self.distribution)
        elif self.toolchain == Toolchain.RUST:
            installer = _RustToolchainInstaller(self.distribution)

        ret = installer.install_toolchain()
        if ret != 0:
            return ret

        return installer.install_additional_tools()


@dataclass(slots=True)
class ToolchainInstallerBuilder:
    '''
    Get the installer based on inputs
    '''
    _toolchain_installer: ToolchainInstaller

    def __init__(self):
        self._toolchain_installer = ToolchainInstaller(None, None)

    def install_toolchain(self, toolchain: Toolchain, path: str = "") -> Self:
        '''
        Specify the toolchain to be installed
        '''

        self._toolchain_installer.toolchain = toolchain
        self._toolchain_installer.install_path = path
        return self

    def install_additional_tools(self, install: bool = False) -> Self:
        '''
        Specify whether to install additional utility tools acoompanied with
        the toolchain
        '''

        self._toolchain_installer.additional_tools = install
        return self

    def distribution(self, distribution: Distribution) -> Self:
        '''
        Specify the distribution
        '''

        self._toolchain_installer.distribution = distribution
        return self

    def build(self) -> ToolchainInstaller:
        '''
        Return the constructed installer
        '''

        return self._toolchain_installer
