'''
PackageManager tests
'''
import os
import unittest

from project_generator.lib.toolchain_manager import (Distribution,
                                                     PackageHandler,
                                                     PackageManagerBuilder)
from project_generator.lib.utils.logger import get_logger

lgr = get_logger('test-pkgmngr')


class TestPackageManagerBuilder(unittest.TestCase):
    '''
    Test suite for the class PackageManagerBuilder
    '''

    def test_build(self):
        '''
        Test case for build function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(True) \
            .distribution(Distribution.ARCH) \
            .build()
        self.assertEqual(
            mngr.cmd_name,
            'pacman'
        )


class TestAptPackageManager(unittest.TestCase):
    '''
    Test suite for the class AptPackageManager
    '''

    def test_install(self):
        '''
        Test the install function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.UBUNTU) \
            .build()
        self.assertEqual(mngr.install(['gcc']).run(), 0)

    def test_update(self):
        '''
        Test the update function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.UBUNTU) \
            .build()
        self.assertEqual(mngr.update(['gcc']).run(), 0)

    def test_remove(self):
        '''
        Test the remove function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(True) \
            .distribution(Distribution.UBUNTU) \
            .build()
        self.assertEqual(mngr.remove(['clang']).run(), 0)


class TestPacmanPackageManager(unittest.TestCase):
    '''
    Test suite for the class PacmanPackageManager
    '''

    def test_install(self):
        '''
        Test the install function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.ARCH) \
            .build()
        self.assertEqual(mngr.install(['gcc', 'clang']).run(), 0)

    def test_update(self):
        '''
        Test the update function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.ARCH) \
            .build()
        self.assertEqual(mngr.update(['gcc']).run(), 0)

    def test_remove(self):
        '''
        Test the remove function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.ARCH) \
            .build()
        self.assertEqual(mngr.remove(['clang']).run(), 0)


class TestYumPackageManager(unittest.TestCase):
    '''
    Test suite for the class YumPackageManager
    '''

    def test_install(self):
        '''
        Test the install function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.RHEL) \
            .build()
        self.assertEqual(mngr.install(['gcc', 'clang']).run(), 0)

    def test_update(self):
        '''
        Test the update function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.RHEL) \
            .build()
        self.assertEqual(mngr.update(['gcc']).run(), 0)

    def test_remove(self):
        '''
        Test the remove function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.RHEL) \
            .build()
        self.assertEqual(mngr.remove(['clang']).run(), 0)


def _check_os() -> PackageHandler | None:
    # read /etc/os-release or /lib/os-release environment file
    os_rel = ''
    for path in ['/etc/os-release', '/usr/lib/os-release']:
        if not os.path.exists(path):
            continue
        os_rel = path
        break

    if os_rel == '':
        raise FileNotFoundError("No 'os-release' found")

    env_dict = {}

    with open(os_rel, encoding='utf8') as rel_file:
        for line in rel_file:
            values = line.strip().split('=')
            if values[0] in ['ID', 'ID_LIKE']:
                env_dict[values[0]] = values[1]

    lgr.debug("Parse env file content: %s", env_dict)
    for item in Distribution:
        if item.name.lower() in [env_dict.get('ID', ""), env_dict.get('ID_LIKE', "")] or \
                item.value in [env_dict.get('ID', ""), env_dict.get('ID_LIKE', "")]:
            return PackageHandler.from_distribution(item)

    return None


if __name__ == '__main__':
    pkg_handler = _check_os()
    if pkg_handler == PackageHandler.APT:
        lgr.debug("PackageHandler = %s", PackageHandler.APT)
        TestAptPackageManager().test_install()
        TestAptPackageManager().test_remove()
        TestAptPackageManager().test_update()
    elif pkg_handler == PackageHandler.PACMAN:
        lgr.debug("PackageHandler = %s", PackageHandler.PACMAN)
        TestPacmanPackageManager().test_install()
        TestPacmanPackageManager().test_remove()
        TestPacmanPackageManager().test_update()
    elif pkg_handler == PackageHandler.YUM:
        lgr.debug("PackageHandler = %s", PackageHandler.YUM)
        TestYumPackageManager().test_install()
        TestYumPackageManager().test_remove()
        TestYumPackageManager().test_update()
    else:
        lgr.warning("No supported distribution detected")
        exit(1)
