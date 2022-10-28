from typing_extensions import Self
from .._distromngr import Distribution, PackageHandler
from .._pkgmngr._pkgmngrif import PackageManager
from .._pkgmngr._pkgmngr import AptPackageManager, PacmanPackageManager


class PackageManagerBuilder:
    '''
    Construct a package manager
    '''

    def __init__(self):
        self._distribution: Distribution = None
        self._confirm: bool = False

    def distribution(self, dist: Distribution) -> Self:
        '''
        Specify the distribution
        '''
        self._distribution = dist
        return self

    def confirm_action(self, cnf: bool) -> Self:
        '''
        Specify whether package manager should ask for confirmation
        '''
        self._confirm = cnf
        return self

    def build(self) -> PackageManager:
        '''
        Return the constructed PackageManager instance
        '''

        handler = PackageHandler.from_distribution(self._distribution)
        pkgmngr = None
        if handler == PackageHandler.APT:
            pkgmngr = AptPackageManager()
        elif handler == PackageHandler.PACMAN:
            pkgmngr = PacmanPackageManager()

        pkgmngr.confirm(self._confirm)

        return pkgmngr
