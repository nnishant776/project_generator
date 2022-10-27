'''
Abstraction for representing Linux distributions
'''

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
        if dist.family == 'debian':
            return PackageHandler.APT
        elif dist.family == 'rhel':
            return PackageHandler.YUM
        elif dist.family == 'suse':
            return PackageHandler.ZYPPER
        elif dist.family == 'arch':
            return PackageHandler.PACMAN
