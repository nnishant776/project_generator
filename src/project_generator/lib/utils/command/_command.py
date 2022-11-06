'''
Command wrapper
'''

import subprocess
import os
from dataclasses import dataclass
from io import BufferedReader
from logging import Logger, StreamHandler
from copy import deepcopy

from typing_extensions import Self

from project_generator.lib.utils.logger import get_logger

lgr = get_logger(module_name="command", stream=StreamHandler())


@dataclass(slots=True, init=True)
class Command:
    '''
    Represents an executable command
    '''

    cmd_name: str
    cmd_opts: list[str]
    cmd_args: list[str]
    sub_cmd: Self
    logger: Logger
    buffered_logging: bool
    env: dict[str, str]
    shell: bool

    def __init__(self, cmd_name="", cmd_opts: list[str] = None, cmd_args: list[str] = None, **kw):
        self.cmd_name: str = cmd_name
        self.cmd_opts = cmd_opts
        self.cmd_args: list[str] = cmd_args
        self.logger: Logger = kw.get('logger', lgr)
        self.buffered_logging: bool = kw.get('buffered_logging', True)
        self.sub_cmd: Self = None
        self.env = None
        self.shell = False

    def programe_name(self) -> str:
        '''
        Return the name of the program to be executed
        '''

        return self.cmd_name

    def args(self) -> list[str]:
        '''
        Return the list of arguments supplied to the program
        '''

        return self.cmd_args

    def flatten(self) -> list[str]:
        '''
        Return the command a simple flat list
        '''

        cmd = []

        if self.env:
            cmd.append('/usr/bin/env')
            for key, value in self.env.items():
                cmd.append(f"{key}={value}")

        cmd.append(self.cmd_name)

        if self.cmd_opts is not None:
            cmd.extend(self.cmd_opts)

        if self.sub_cmd is not None:
            cmd.extend(self.sub_cmd.flatten())

        if self.cmd_args is not None:
            cmd.extend(self.cmd_args)

        return cmd

    def run(self) -> int:
        '''
        Run the command
        '''

        return _check_call(
            self.flatten(),
            buffered_out=self.buffered_logging,
            logger=self.logger,
            env=self.env,
            shell=self.shell
        )


class CommandBuilder:
    '''
    Helper class to create a `Command` instance
    '''

    def __init__(self):
        self._command = Command(cmd_name="")

    def program(self, name: str) -> Self:
        '''
        Name of the program to be run
        '''

        if name == "":
            raise ValueError("empty command name")
        if self._command.cmd_name != "" and self._command.cmd_name is not None:
            raise ValueError("cannot reassign command name")

        self._command.cmd_name = name
        return self

    def subcommand(self, sub_cmd: Command) -> Self:
        '''
        Append a subcommand as part of the original command
        '''

        self._command.sub_cmd = sub_cmd
        return self

    def option(self, opt: str) -> Self:
        '''
        Add an option on the original command
        '''

        if self._command.cmd_opts is None:
            self._command.cmd_opts = []
        self._command.cmd_opts.append(opt)
        return self

    def options(self, opts: list[str]) -> Self:
        '''
        Add multiple options on the original command
        '''

        if self._command.cmd_opts is None:
            self._command.cmd_opts = []
        self._command.cmd_opts.extend(opts)
        return self

    def arg(self, arg: str) -> Self:
        '''
        Append an argument to the command
        '''

        if self._command.cmd_args is None:
            self._command.cmd_args = []
        self._command.cmd_args.append(arg)
        return self

    def args(self, arg_list: list[str]) -> Self:
        '''
        Append a multiple arguments to the command
        '''

        if self._command.cmd_args is None:
            self._command.cmd_args = []
        self._command.cmd_args.extend(arg_list)
        return self

    def capture_logs(self, buffered: bool = True) -> Self:
        '''
        Specify whether to capture logs when running the command
        '''

        self._command.buffered_logging = buffered
        return self

    def env_vars(self, env: dict[str, str]) -> Self:
        '''
        Specify the environment variables for this command
        '''

        self._command.env = deepcopy(env)
        return self

    def invoke_shell(self, shell: bool = False) -> Self:
        '''
        Specify whether to run the command inside a shell
        '''

        self._command.shell = shell
        return self

    def build(self) -> Command:
        '''
        Return the constructed command
        '''

        return self._command


def _check_call(*args, buffered_out: bool = True, **kw_args) -> int:
    '''
    Wrapper to intercept and forward the call to subprocess module
    '''
    logger = lgr
    env = deepcopy(os.environ)
    use_shell = False

    if kw_args:
        _logger = kw_args.get('logger', None)
        if _logger is not None:
            logger = _logger

        _env = kw_args.get('env', None)
        if _env is not None:
            env.update(_env)

        use_shell = kw_args.get('shell', False)

    logger.debug("Command: %s", *args)

    ret = 0

    try:
        stdout_file = subprocess.PIPE
        stderr_file = subprocess.STDOUT

        with subprocess.Popen(
            *args,
            env=env,
            stdout=stdout_file,
            stderr=stderr_file,
            shell=use_shell,
        ) as process:
            if process.stdout is not None:
                with process.stdout as out:
                    if not buffered_out:
                        reader = out
                    else:
                        reader = BufferedReader(out)
                    for line in iter(reader.readline, b''):
                        logger.debug(
                            "(%s) - %s", process.args[0], line.decode('utf-8').strip())
                    process.stdout.flush()

                ret = process.wait()
                logger.debug("(%s) - Process returned %d",
                             process.args[0], ret)

    except FileNotFoundError as exec_err:
        logger.debug(
            "Failed to find executable '%s'. Process returned '%d'.",
            exec_err.filename,
            exec_err.errno,
        )
        ret = exec_err.errno

    except subprocess.CalledProcessError as run_err:
        logger.debug(
            "Failed to run command '%s'. Process returned '%d' with output: '%s'",
            ' '.join(*args),
            run_err.returncode,
            run_err.output,
        )
        ret = run_err.returncode

    return ret
