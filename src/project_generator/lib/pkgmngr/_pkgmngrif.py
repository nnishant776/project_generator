'''
Interface for package manager
'''

from dataclasses import dataclass
from enum import Enum

from typing_extensions import Self

from project_generator.lib.utils.command import Command


class Action(Enum):
    '''
    An enum listing the supported actions for a package manager
    '''
    INSTALL = 'install'
    REMOVE = 'remove'
    UPDATE = 'update'


@dataclass(slots=True, init=True, kw_only=True)
class PackageManager:
    '''
    Abstraction to represent a package manager
    '''

    confirmation: bool = None
    action: Action = None
    pkglist: dict[str, Action] = None
    cmd_name: str = None
    synced: bool = None
    command_list: list[Command] = None

    def __init__(self):
        self.confirmation = False
        self.action = None
        self.cmd_name = None
        self.synced = False
        self.command_list: list[Command] = []
        self.pkglist = {}

    def confirm(self, cnf: bool = False) -> Self:
        '''
        Whether to ask confirmation for an action
        '''
        self.confirmation = cnf
        return self

    def install(self, install_list: list[str]) -> Self:
        '''
        Install the given list of packages
        '''
        return self

    def remove(self, remove_list: list[str]) -> Self:
        '''
        Remove the given list of packages
        '''
        return self

    def update(self, update_list: list[str]) -> Self:
        '''
        Update all or the selected list of packages
        '''
        return self

    def sync(self, sync_repo: bool = False) -> Self:
        '''
        Sync the repository metadata
        '''
        return self

    def command(self) -> list[Command]:
        '''
        Return the raw accumulated commands so far
        '''
        return self.command_list

    def commit(self) -> int:
        '''
        Run the package manager commands
        '''
        return 0
