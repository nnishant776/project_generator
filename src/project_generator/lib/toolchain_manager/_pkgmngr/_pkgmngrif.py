'''
Interface for package manager
'''

from enum import Enum
from dataclasses import dataclass

from typing_extensions import Self


class Action(Enum):
    '''
    An enum listing the supported actions for a package manager
    '''
    INSTALL = 'install'
    REMOVE = 'remove'
    UPDATE = 'update'


@dataclass(slots=True, init=True)
class PackageManager:
    '''
    Abstraction to represent a package manager
    '''

    confirmation: bool = None
    action: Action = None
    pkglist: dict[str, Action] = {}
    cmd_name: str = None
        self.cmd_name: str = None

    def confirm(self, cnf: bool = False) -> Self:
        '''
        Whether to ask confirmation for an action
        '''
        self.confirmation = cnf
        return self

    def install(self, pkglist: list[str]) -> Self:
        '''
        Install the given list of packages
        '''
        for pkg in pkglist:
            val = self.pkglist.get(pkg)
            if val is None:
                self.pkglist[pkg] = Action.INSTALL
            elif val == Action.REMOVE:
                raise ValueError(
                    f"Package {pkg} listed in at least 2 conflicting actions")
        return self

    def remove(self, pkglist: list[str]) -> Self:
        '''
        Remove the given list of packages
        '''
        for pkg in pkglist:
            val = self.pkglist.get(pkg)
            if val is None:
                self.pkglist[pkg] = Action.REMOVE
            elif val in [Action.INSTALL, Action.UPDATE]:
                raise ValueError(
                    f"Package {pkg} listed in at least 2 conflicting actions")
        return self

    def update(self, _: list[str] = None) -> Self:
        '''
        Update all or the selected list of packages
        '''
        return self

    def run(self) -> int:
        '''
        Run the package manager commands
        '''
        return 0
