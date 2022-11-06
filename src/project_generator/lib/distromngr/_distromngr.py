'''
Abstraction for representing Linux distributions
'''

import os

from enum import Enum


class Distribution(Enum):
    '''
    An enum representing the different Linux distributions with the
    corresponding values representing the distribution family
    '''
    UBUNTU = 'debian'
    FEDORA = 'rhel'
    RHEL = 'rhel'
    DEBIAN = 'debian'
    OPENSUSE = 'suse'
    ARCH = 'arch'
    MANJARO = 'arch'

    @property
    def family(self):
        '''
        Get the distribution family for the selected distribution
        '''
        return self.value


class PackageHandler(Enum):
    '''
    An enum denoting the package handler application
    '''
    APT = 'apt-get'
    YUM = 'yum'
    ZYPPER = 'zypper'
    PACMAN = 'pacman'

    @staticmethod
    def from_distribution(dist: Distribution):
        '''
        Get the package handler based on the distribution
        '''
        if dist is not None:
            if dist.family == 'debian':
                return PackageHandler.APT
            if dist.family == 'rhel':
                return PackageHandler.YUM
            if dist.family == 'suse':
                return PackageHandler.ZYPPER
            if dist.family == 'arch':
                return PackageHandler.PACMAN

        return None


def get_distribution() -> Distribution | None:
    '''
    Get the distribution after parsing the /etc/os-release file
    '''
    # read /etc/os-release or /lib/os-release environment file
    os_rel = ''
    for path in ['/etc/os-release', '/usr/lib/os-release']:
        if not os.path.exists(path):
            continue
        os_rel = path
        break

    if os_rel == '':
        raise FileNotFoundError("No release info found")

    env_dict = {}

    with open(os_rel, encoding='utf-8') as rel_file:
        for line in rel_file:
            values = line.strip().split('=')
            if values[0] in ['ID', 'ID_LIKE']:
                env_dict[values[0]] = values[1]

    dists = []
    for _, value in env_dict.items():
        dists.append(str(value).lower())

    for item in Distribution:
        if item.name.lower() in dists or item.value.lower() in dists:
            return item

    return None
