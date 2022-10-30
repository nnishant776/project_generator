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
            .confirm_action(False) \
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
        mngr.install(['gcc'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "apt-get", "-y", "install",  "gcc"])

        if _check_os() == PackageHandler.APT:
            self.assertEqual(mngr.commit(), 0)

    def test_update(self):
        '''
        Test the update function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.UBUNTU) \
            .build()
        mngr.update(['gcc'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "apt-get", "-y", "upgrade",  "gcc"])

        if _check_os() == PackageHandler.APT:
            self.assertEqual(mngr.commit(), 0)

    def test_remove(self):
        '''
        Test the remove function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.UBUNTU) \
            .build()
        mngr.remove(['clang'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "apt-get", "-y", "remove",  "clang"])

        if _check_os() == PackageHandler.APT:
            self.assertEqual(mngr.commit(), 0)

    def test_sync(self):
        '''
        Test the sync function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.UBUNTU) \
            .build()
        mngr.sync(True)
        self.assertEqual(mngr.command()[0].flatten(), [
                         "apt-get", "-y", "update"])

        if _check_os() == PackageHandler.APT:
            self.assertEqual(mngr.commit(), 0)

    def test_sync_and_upgrade(self):
        '''
        Test the sync function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.UBUNTU) \
            .build()
        mngr.sync(True)
        mngr.update(['gcc'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "apt-get", "-y", "update"])

        self.assertEqual(mngr.command()[1].flatten(), [
                         "apt-get", "-y", "upgrade", "gcc"])

        if _check_os() == PackageHandler.APT:
            self.assertEqual(mngr.commit(), 0)


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
        mngr.install(['gcc'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "pacman", "--noconfirm", "-S",  "gcc"])

        if _check_os() == PackageHandler.PACMAN:
            self.assertEqual(mngr.commit(), 0)

    def test_update(self):
        '''
        Test the update function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.ARCH) \
            .build()
        mngr.update(['gcc'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "pacman", "--noconfirm", "-Su",  "gcc"])

        if _check_os() == PackageHandler.PACMAN:
            self.assertEqual(mngr.commit(), 0)

    def test_remove(self):
        '''
        Test the remove function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.ARCH) \
            .build()
        mngr.remove(['clang'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "pacman", "--noconfirm", "-Rcs",  "clang"])

        if _check_os() == PackageHandler.PACMAN:
            self.assertEqual(mngr.commit(), 0)

    def test_sync(self):
        '''
        Test the sync function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.ARCH) \
            .build()
        mngr.sync(True)
        self.assertEqual(mngr.command()[0].flatten(), [
                         "pacman", "--noconfirm", "-Sy"])

        if _check_os() == PackageHandler.PACMAN:
            self.assertEqual(mngr.commit(), 0)

    def test_sync_and_upgrade(self):
        '''
        Test the sync function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.ARCH) \
            .build()
        mngr.sync(True)
        mngr.update(['gcc'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "pacman", "--noconfirm", "-Sy"])

        self.assertEqual(mngr.command()[1].flatten(), [
                         "pacman", "--noconfirm", "-Su", "gcc"])

        if _check_os() == PackageHandler.PACMAN:
            self.assertEqual(mngr.commit(), 0)


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
        mngr.install(['gcc'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "yum", "-y", "install",  "gcc"])

        if _check_os() == PackageHandler.YUM:
            self.assertEqual(mngr.commit(), 0)

    def test_update(self):
        '''
        Test the update function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.RHEL) \
            .build()
        mngr.update(['gcc'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "yum", "-y", "upgrade",  "gcc"])

        if _check_os() == PackageHandler.YUM:
            self.assertEqual(mngr.commit(), 0)

    def test_remove(self):
        '''
        Test the remove function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.RHEL) \
            .build()
        mngr.remove(['clang'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "yum", "-y", "remove",  "clang"])

        if _check_os() == PackageHandler.YUM:
            self.assertEqual(mngr.commit(), 0)

    def test_sync(self):
        '''
        Test the sync function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.RHEL) \
            .build()
        mngr.sync(True)
        self.assertEqual(mngr.command()[0].flatten(), [
                         "yum", "-y", "makecache"])

        if _check_os() == PackageHandler.YUM:
            self.assertEqual(mngr.commit(), 0)

    def test_sync_and_upgrade(self):
        '''
        Test the sync function
        '''
        mngr = PackageManagerBuilder() \
            .confirm_action(False) \
            .distribution(Distribution.RHEL) \
            .build()
        mngr.sync(True)
        mngr.update(['gcc'])
        self.assertEqual(mngr.command()[0].flatten(), [
                         "yum", "-y", "makecache"])

        self.assertEqual(mngr.command()[1].flatten(), [
                         "yum", "-y", "upgrade", "gcc"])

        if _check_os() == PackageHandler.YUM:
            self.assertEqual(mngr.commit(), 0)


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
    unittest.main()
