'''
Test module for toolchain installer
'''

import unittest

from project_generator.lib.toolchain import Toolchain
from project_generator.lib.distromngr import Distribution
from project_generator.lib.toolchain_manager.installer import ToolchainInstallerBuilder


class TestToolchainInstaller(unittest.TestCase):
    '''
    Test suite for toolchain installer
    '''

    def test_c_installer(self):
        '''
        Test the installation for C toolchain
        '''
        installer = ToolchainInstallerBuilder().distribution(
            Distribution.FEDORA).install_toolchain(Toolchain.C).build()
        self.assertEqual(installer.install_toolchain(), 0)


if __name__ == '__main__':
    TestToolchainInstaller().test_c_installer()
