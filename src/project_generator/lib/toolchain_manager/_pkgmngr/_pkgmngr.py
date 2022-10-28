'''
PackageManager implementations
'''

import subprocess
from io import BufferedReader

from project_generator.lib.utils import logger

from ._pkgmngrif import Action, PackageManager

lgr = logger.get_logger('pkgmngr')


def check_call(*args, buffered_out: bool = True, **kw_args) -> int:
    '''
    Wrapper to intercept and forward the call to subprocess module
    '''
    lgr.debug("Command: %s", *args)
    ret = 0
    try:
        stdout_file = None
        stderr_file = None

        if lgr.isEnabledFor(logging.DEBUG):
            stdout_file = subprocess.PIPE
            stderr_file = subprocess.STDOUT
        else:
            stdout_file = subprocess.DEVNULL
            stderr_file = subprocess.STDOUT

        process = subprocess.Popen(
            *args, stdout=stdout_file, stderr=stderr_file, **kw_args)

        if process.stdout is not None:
            with process.stdout as out:
                if not buffered_out:
                    reader = out
                else:
                    reader = BufferedReader(out)
                for line in iter(reader.readline, b''):
                    lgr.debug(
                        "(%s) - %s", process.args[0], line.decode('utf8').strip())
                process.stdout.flush()

        ret = process.wait()
        lgr.debug("(%s) - Process returned %d", process.args[0], ret)

    except FileNotFoundError as exec_err:
        lgr.fatal("Failed to find executable '%s'", exec_err.filename)
    except subprocess.CalledProcessError as run_err:
        lgr.error(
            "Failed to run command '%s'. Process returned '%d' with output: '%s'", ' '.join(*args), run_err.returncode, run_err.output)
        ret = run_err.returncode

    return ret


class AptPackageManager(PackageManager):
    '''
    Package manager implementation for Apt for debian based distros
    '''

    def __init__(self, *args, **kw_args):
        PackageManager.__init__(self, *args, **kw_args)
        self.cmd_name = 'apt-get'

    def run(self):
        '''
        Run the built command
        '''
        install_bucket: list[str] = []
        remove_bucket: list[str] = []
        update_bucket: list[str] = []

        for key, val in self.pkglist.items():
            if val == Action.INSTALL:
                install_bucket.append(key)
            elif val == Action.REMOVE:
                remove_bucket.append(key)
            elif val == Action.UPDATE:
                update_bucket.append(key)

        cmd = [self.cmd_name]

        if not self.confirmation:
            cmd.append("-y")

        ret = 0
        buffered_out = True

        if self.confirmation:
            buffered_out = False

        cmd_install = [*cmd]
        if len(install_bucket) > 0:
            cmd_install.append("install")
            cmd_install.extend(install_bucket)
            ret = check_call(cmd_install, buffered_out=buffered_out)

        cmd_remove = [*cmd]
        if len(remove_bucket) > 0:
            cmd_remove.append("remove")
            cmd_remove.extend(remove_bucket)
            ret = check_call(cmd_remove, buffered_out=buffered_out)

        cmd_update = [*cmd]
        if len(update_bucket) > 0:
            cmd_update.append("update")
            ret = check_call(cmd_update, buffered_out=buffered_out)
            cmd_upgrade = [*cmd]
            cmd_upgrade.append("upgrade")
            cmd_upgrade.extend(update_bucket)
            ret = check_call(cmd_upgrade, buffered_out=buffered_out)

        return ret


class PacmanPackageManager(PackageManager):
    '''
    Package manager implementation for Pacman for debian based distros
    '''

    def __init__(self):
        PackageManager.__init__(self)
        self.cmd_name = 'pacman'

    def run(self) -> int:
        '''
        Run the built command
        '''
        install_bucket: list[str] = []
        remove_bucket: list[str] = []
        update_bucket: list[str] = []

        for key, val in self.pkglist.items():
            if val == Action.INSTALL:
                install_bucket.append(key)
            elif val == Action.REMOVE:
                remove_bucket.append(key)
            elif val == Action.UPDATE:
                update_bucket.append(key)

        cmd = [self.cmd_name]

        if not self.confirmation:
            cmd.append("--noconfirm")

        ret = 0
        buffered_out = True

        if self.confirmation:
            buffered_out = False

        cmd_install = [*cmd]
        if len(install_bucket) > 0:
            cmd_install.append("-S")
            cmd_install.extend(install_bucket)
            ret = check_call(cmd_install, buffered_out=buffered_out)

        cmd_remove = [*cmd]
        if len(remove_bucket) > 0:
            cmd_remove.append("-Rcs")
            cmd_remove.extend(remove_bucket)
            ret = check_call(cmd_remove, buffered_out=buffered_out)

        cmd_update = [*cmd]
        if len(update_bucket) > 0:
            cmd_update.append("-Su")
            cmd_update.extend(update_bucket)
            ret = check_call(cmd_update, buffered_out=buffered_out)

        return ret
