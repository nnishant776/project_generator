'''
    Package manager implementation for Apt for debian based distros
'''

from dataclasses import dataclass

from typing_extensions import Self

from project_generator.lib.utils.command import Command, CommandBuilder

from ._pkgmngrif import PackageManager


@dataclass(slots=True, init=True)
class AptPackageManager(PackageManager):
    '''
    Package manager implementation for Apt for debian based distros
    '''

    def __init__(self, *args, **kw_args):
        PackageManager.__init__(self, *args, **kw_args)
        self.cmd_name = 'apt-get'

    def _partial_cmd(self) -> CommandBuilder:
        cmd = CommandBuilder()
        cmd.program(self.cmd_name)
        if not self.confirmation:
            cmd.option("-y")
        cmd.capture_logs(buffered=not self.confirmation)

        return cmd

    def sync(self, sync_repo: bool = False) -> Self:
        if sync_repo:
            cmd_sync = self._partial_cmd()
            cmd_sync.subcommand(Command(cmd_name="update"))
            self.synced = True
            self.command_list.append(cmd_sync.build())

        return self

    def install(self, install_list: list[str]) -> Self:
        if not self.synced:
            self.sync(True)

        if len(install_list) > 0:
            cmd_install = self._partial_cmd()
            cmd_install.subcommand(Command(cmd_name="install"))
            cmd_install.args(install_list)

            self.command_list.append(cmd_install.build())

        return self

    def remove(self, remove_list: list[str]) -> Self:
        if len(remove_list) > 0:
            cmd_remove = self._partial_cmd()
            cmd_remove.subcommand(Command(cmd_name="remove"))
            cmd_remove.args(remove_list)

            self.command_list.append(cmd_remove.build())

        return self

    def update(self, update_list: list[str]) -> Self:
        if len(update_list) > 0:
            cmd_update = self._partial_cmd()
            cmd_update.subcommand(Command(cmd_name="upgrade"))
            cmd_update.args(update_list)

            self.command_list.append(cmd_update.build())

        return self

    def commit(self):
        '''
        Run the built command
        '''
        for cmd in self.command_list:
            ret = cmd.run()
            if ret != 0:
                return ret

        return 0
