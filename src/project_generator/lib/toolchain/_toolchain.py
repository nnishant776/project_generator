'''
Abstraction for a toolchain
'''

from enum import Enum
from copy import deepcopy

from project_generator.lib.distromngr import Distribution
from ._distro_pkglist import _toolchain_packages


class Toolchain(Enum):
    '''
    An enumeration listing all the supported toolchains
    '''
    C = 'c'
    CPP = 'cpp'
    RUST = 'rust'
    GO = 'go'
    GTK = 'gtk'
    PYTHON = 'python'

    def packages_for(self, distribution: Distribution) -> list[str]:
        '''
        Get the list of packages for the current toolchain
        '''

        pkg_registry: dict[str, str] = _toolchain_packages.get(
            distribution.family, None)
        if pkg_registry is None:
            raise ValueError(
                f"Distribution {distribution.value} is not supported")

        pkg_list: list[str] = deepcopy(pkg_registry.get(self.value, None))

        if pkg_list is None:
            raise ValueError(f"Invalid toolchain {self.value}")

        pkg_list.extend(pkg_registry.get('base'))

        if self == Toolchain.CPP:
            pkg_list.extend(pkg_registry.get(Toolchain.C.value, None))
        elif self == Toolchain.GTK:
            pkg_list.extend(pkg_registry.get(Toolchain.C.value, None))
            pkg_list.extend(pkg_registry.get(Toolchain.CPP.value, None))
        elif self == Toolchain.GO:
            pkg_list.extend(pkg_registry.get(Toolchain.C.value, None))
            pkg_list.extend(pkg_registry.get(Toolchain.CPP.value, None))
        elif self == Toolchain.RUST:
            pkg_list.extend(pkg_registry.get(Toolchain.C.value, None))
            pkg_list.extend(pkg_registry.get(Toolchain.CPP.value, None))

        return pkg_list
