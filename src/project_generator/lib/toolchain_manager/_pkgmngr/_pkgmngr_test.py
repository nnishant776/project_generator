import os
import unittest

from project_generator.lib.toolchain_manager import (Distribution,
                                                     PackageHandler,
                                                     PackageManagerBuilder)
from project_generator.lib.toolchain_manager._pkgmngr._pkgmngr import \
    PacmanPackageManager
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
            PacmanPackageManager().cmd_name
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
        mngr.install(['gcc']).run()

    def test_update(self):
        '''
        Test the update function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.UBUNTU) \
            .build()
        mngr.update(['gcc']).run()

    def test_remove(self):
        '''
        Test the remove function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(True) \
            .distribution(Distribution.UBUNTU) \
            .build()
        mngr.remove(['clang']).run()


class TestPacmanPackageManager(unittest.TestCase):
    '''
    Test suite for the class AptPackageManager
    '''

    def test_install(self):
        '''
        Test the install function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.ARCH) \
            .build()
        mngr.install(['gcc', 'clang']).run()

    def test_update(self):
        '''
        Test the update function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.ARCH) \
            .build()
        mngr.update(['gcc']).run()

    def test_remove(self):
        '''
        Test the remove function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(True) \
            .distribution(Distribution.ARCH) \
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
        if item.name.lower() in [env_dict['ID'], env_dict['ID_LIKE']] or \
                item.value in [env_dict['ID'], env_dict['ID_LIKE']]:
            return PackageHandler.from_distribution(item)

    return None


if __name__ == '__main__':
    unittest.main()
