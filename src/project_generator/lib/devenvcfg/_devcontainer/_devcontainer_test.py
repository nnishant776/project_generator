'''
DevContainer test suite
'''

import io
import unittest

import yaml
from project_generator.lib import devenvcfg
from project_generator.lib.devenvcfg._devcontainer._devcontainer import \
    DevContainerBuilder, DevContainer

from project_generator.lib.utils.logger import get_logger


logger = get_logger("devcontainer_test")


class TestDevcontainerDumpYaml(unittest.TestCase):
    '''
    Test suite for testing YAML serialization of DevContainer class
    '''

    def test_yaml_dump(self):
        '''
        Test YAML dump
        '''
        container = DevContainerBuilder() \
            .container_image('ubuntu:latest') \
            .container_name('vscode-ubuntu') \
            .override_command(True) \
            .user_env_probe(False) \
            .remote_user('root') \
            .capabilities(["SYS_PTRACE", "SYS_NET_ADMIN"]) \
            .build_spec_from_args(dockerfile="Dockerfile", context='.') \
            .mounts([
                devenvcfg.devcontainer.MountSpec(source='/home/neeraj'),
                devenvcfg.devcontainer.MountSpec(source='/etc/passwd'),
            ]) \
            .container_user('root') \
            .build()
        logger.debug("---------------- test_yaml_dump ----------------")

        logger.debug(yaml.safe_dump(
            data={'devcontainer': container.serialize()}, stream=None))

    def test_yaml_load(self):
        '''
        Test YAML load
        '''
        container = DevContainerBuilder() \
            .container_image('ubuntu:latest') \
            .container_name('vscode-ubuntu') \
            .override_command(True) \
            .user_env_probe(False) \
            .remote_user('root') \
            .capabilities(["SYS_PTRACE", "SYS_NET_ADMIN"]) \
            .build_spec_from_args(dockerfile="Dockerfile", context=".") \
            .mounts([
                devenvcfg.devcontainer.MountSpec(source='/home/neeraj'),
                devenvcfg.devcontainer.MountSpec(source='/etc/passwd'),
            ]) \
            .container_user('root') \
            .build()
        container_serialized = container.serialize()
        container_yaml = yaml.safe_dump(container_serialized, stream=None)

        logger.debug("---------------- test_yaml_load ----------------")
        logger.debug("container_original=%s", container)
        logger.debug("container_serialized=%s", container_serialized)
        logger.debug("container_yaml=%s", container_yaml)

        str_reader = io.StringIO(container_yaml)
        container_deserialized = yaml.safe_load(str_reader)

        logger.debug("container_deserialized=%s", container_deserialized)

        self.assertEqual(container_serialized, container_deserialized)

        val = DevContainer.from_dict(container_deserialized)

        logger.debug("container_recreated=%s", val)

        self.assertEqual(val, container)


if __name__ == '__main__':
    unittest.main()
