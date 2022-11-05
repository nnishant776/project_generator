'''
Module for installing the configured toolchains for the project
'''

from dataclasses import dataclass

from typing_extensions import Self

from project_generator.lib.toolchain import Toolchain
from project_generator.lib.distromngr import Distribution
from project_generator.lib.pkgmngr import PackageManagerBuilder


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
        else:
            return Installer(self._distribution)
