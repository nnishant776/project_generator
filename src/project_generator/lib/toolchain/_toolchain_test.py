'''
Test module for Toolchain
'''

import unittest

from project_generator.lib.distromngr import Distribution

from ._distro_pkglist import _extra_tools_packages, _toolchain_packages
from ._toolchain import Toolchain


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
        self.assertEqual(pkg_list, [
            *_toolchain_packages['rhel']['cpp'],
            *_toolchain_packages['rhel']['base'],
            *_toolchain_packages['rhel']['c'],
        ])

    def test_arch_gcc(self):
        '''
        Test case for Arch and CPP toolchain
        '''

        toolchain = Toolchain.CPP
        pkg_list = toolchain.packages_for(Distribution.ARCH)
        self.assertEqual(pkg_list, [
            *_toolchain_packages['arch']['cpp'],
            *_toolchain_packages['arch']['base'],
            *_toolchain_packages['arch']['c'],
        ])

    def test_debian_gcc(self):
        '''
        Test case for Debian and CPP toolchain
        '''

        toolchain = Toolchain.CPP
        pkg_list = toolchain.packages_for(Distribution.DEBIAN)
        self.assertEqual(pkg_list, [
            *_toolchain_packages['debian']['cpp'],
            *_toolchain_packages['debian']['base'],
            *_toolchain_packages['debian']['c'],
        ])

    def test_extrapkg_rhel_gcc(self):
        '''
        Test case for RHEL and CPP toolchain
        '''

        toolchain = Toolchain.CPP
        pkg_list = toolchain.extra_packages_for(Distribution.RHEL)
        self.assertEqual(pkg_list, [
            *_extra_tools_packages['rhel']['cpp'],
            *_extra_tools_packages['rhel']['c'],
        ])

    def test_extrapkg_arch_gcc(self):
        '''
        Test case for Arch and CPP toolchain
        '''

        toolchain = Toolchain.CPP
        pkg_list = toolchain.extra_packages_for(Distribution.ARCH)
        self.assertEqual(pkg_list, [
            *_extra_tools_packages['arch']['cpp'],
            * _extra_tools_packages['arch']['c'],
        ])

    def test_extrapkg_debian_gcc(self):
        '''
        Test case for Debian and CPP toolchain
        '''

        toolchain = Toolchain.CPP
        pkg_list = toolchain.extra_packages_for(Distribution.DEBIAN)
        self.assertEqual(pkg_list, [
            *_extra_tools_packages['debian']['cpp'],
            *_extra_tools_packages['debian']['c'],
        ])


if __name__ == '__main__':
    unittest.main()
