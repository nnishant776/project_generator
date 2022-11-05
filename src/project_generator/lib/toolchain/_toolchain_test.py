'''
Test module for Toolchain
'''

import unittest

from project_generator.lib.distromngr import Distribution
from ._toolchain import Toolchain
from ._distro_pkglist import _toolchain_packages


class TestToolchain(unittest.TestCase):
    '''
    Test suite for Toolchain class
    '''

    def test_rhel_gcc(self):
        '''
        Test case for RHEL and CPP toolchain
        '''
        toolchain = Toolchain.CPP
        pkg_list = toolchain.packages_for(Distribution.RHEL)
        print(pkg_list)
        print(_toolchain_packages['rhel']['cpp'])
        self.assertEqual(pkg_list, [*_toolchain_packages['rhel']['cpp'], *
                         _toolchain_packages['rhel']['base'], *_toolchain_packages['rhel']['c']])


if __name__ == '__main__':
    TestToolchain().test_rhel_gcc()
