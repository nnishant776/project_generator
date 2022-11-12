'''
Test module for toolchain installer
'''

import unittest

from project_generator.lib.distromngr import get_distribution
from project_generator.lib.toolchain import Toolchain
from project_generator.lib.toolchain_manager.installer import \
    ToolchainInstallerBuilder


class TestToolchainInstaller(unittest.TestCase):
    '''
    Test suite for toolchain installer
    '''

    def test_c_installer(self):
        '''
        Test the installation for C toolchain
        '''

        distro = get_distribution()
        if distro is not None:
            installer = ToolchainInstallerBuilder().distribution(
                distro).install_toolchain(Toolchain.C).build()
            self.assertEqual(installer.run(), 0)

    def test_cpp_installer(self):
        '''
        Test the installation for C++ toolchain
        '''

        distro = get_distribution()
        if distro is not None:
            installer = ToolchainInstallerBuilder().distribution(
                distro).install_toolchain(Toolchain.CPP).build()
            self.assertEqual(installer.run(), 0)

    def test_gtk_installer(self):
        '''
        Test the installation for Gtk toolchain
        '''

        distro = get_distribution()
        if distro is not None:
            installer = ToolchainInstallerBuilder().distribution(
                distro).install_toolchain(Toolchain.GTK).build()
            self.assertEqual(installer.run(), 0)

    def test_go_installer(self):
        '''
        Test the installation for Go toolchain
        '''
        installer = ToolchainInstallerBuilder().distribution(
            None).install_toolchain(Toolchain.GO).build()
        self.assertEqual(installer.run(), 0)

    def test_rust_installer(self):
        '''
        Test the installation for Rust toolchain
        '''
        installer = ToolchainInstallerBuilder().distribution(
            None).install_toolchain(Toolchain.RUST).build()
        self.assertEqual(installer.run(), 0)


if __name__ == '__main__':
    TestToolchainInstaller().test_go_installer()
