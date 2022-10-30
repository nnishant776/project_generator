'''
Unit tests for command package
'''

import unittest

from project_generator.lib.utils.command._command import CommandBuilder, Command


class TestCommandBuilder(unittest.TestCase):
    '''
    Test suite for `CommandBuilder`
    '''

    def test_command_build(self):
        '''
        Test `build()` function
        '''
        cmd = CommandBuilder().program("apt-get").option(
            "-y").subcommand(Command("update", None, None)).build()

        self.assertEqual(cmd.cmd_name, "apt-get")
        self.assertEqual(cmd.cmd_opts[0], "-y")
        self.assertEqual(cmd.sub_cmd.cmd_name, "update")
        self.assertEqual(cmd.flatten(), ["apt-get", "-y", "update"])
        # self.assertEqual(cmd.run(), 0)

    def test_command_build_multiargs(self):
        '''
        Test `build()` function
        '''
        cmd = CommandBuilder().program("apt-get").option(
            "-y").subcommand(Command("install")).args(["gcc", "clang", "git"]).build()

        self.assertEqual(cmd.cmd_name, "apt-get")
        self.assertEqual(cmd.cmd_opts[0], "-y")
        self.assertEqual(cmd.sub_cmd.cmd_name, "install")
        self.assertEqual(cmd.cmd_args[0], "gcc")
        self.assertEqual(cmd.cmd_args[1], "clang")
        self.assertEqual(cmd.cmd_args[2], "git")
        self.assertEqual(
            cmd.flatten(), ["apt-get", "-y", "install", "gcc", "clang", "git"])

    def test_solo_command(self):
        '''
        Test a single command without any args
        '''
        cmd = CommandBuilder().program("ls").build()

        self.assertEqual(cmd.cmd_name, "ls")
        self.assertEqual(cmd.cmd_opts, None)
        self.assertEqual(cmd.cmd_args, None)
        self.assertEqual(cmd.sub_cmd, None)
        self.assertEqual(cmd.flatten(), ["ls"])
        self.assertEqual(cmd.run(), 0)


if __name__ == '__main__':
    unittest.main()
