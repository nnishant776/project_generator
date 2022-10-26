'''
Module which configures a devcontaner specification
'''

from dataclasses import dataclass
from enum import Enum
from typing_extensions import Self
from lib.utils.json import Serializer, TransformType


class ContainerRuntime(Enum):
    '''
    An enum defining the list of supported container runtimes
    '''
    DOCKER = 'docker'
    PODMAN = 'podman'


class MountType(Enum):
    '''
    An enum defining different types of mount types available
    '''
    BIND = 'bind'
    VOLUME = 'volume'

    def to_json(self):
        '''
        Return json obeject repr for MountType
        '''
        return self.value


@dataclass(slots=True)
class MountSpec:
    '''
    Mount definition for dev container
    '''
    source: str
    target: str
    type: MountType

    def __init__(self, source: str, target: str | None = None, mount_type: MountType | None = None):
        self.source = source
        if target is None or target == '':
            self.target = self.source
        if mount_type is None:
            self.type = MountType.BIND


@dataclass(slots=True)
class ContainerBuildSpec:
    '''
    A class representing the json spec for building the dev container
    '''

    dockerfile: str
    context: str
    args: dict = None
    target: str = None
    cache_from: str | list[str] = None


@dataclass(slots=True)
class DevContainer:
    '''
    Reprsents the devcontainer configuration
    '''

    name: str = None
    image: str = None
    remote_user: str = 'root'
    container_user: str = 'root'
    remote_env: dict[str, str] = None
    container_env: dict[str, str] = None
    build: ContainerBuildSpec = None
    forward_ports: list[int] = None
    override_command: bool = True
    privileged: bool = False
    security_opt: list[str] = None
    cap_add: list[str] = None
    mounts: list[MountSpec] = None
    workspace_mount: str = None
    workspace_folder: str = None
    run_args: list[str] = None
    extensions: list[str] = None

    def to_json(self):
        '''
        Return a JSON repr of dev container
        '''
        return Serializer(transform_keys=TransformType.CAMEL_CASE, bypass=True).default(self)


class DevContainerBuilder:
    '''
    A helper class to build a `DevContainer` object
    '''

    def __init__(self):
        self._devcontainer: DevContainer = DevContainer()

    def container_name(self, name: str) -> Self:
        '''
        Specify the name of the container being built
        '''
        self._devcontainer.name = name
        return self

    def container_image(self, image_name: str) -> Self:
        '''
        Specify the docker image name on which the container will be based on
        '''
        self._devcontainer.image = image_name
        return self

    def remote_user(self, remote_user: str) -> Self:
        '''
        Specify the remote user for the devcontainer
        '''
        self._devcontainer.remote_user = remote_user
        return self

    def container_user(self, container_user: str) -> Self:
        '''
        Specify the container user for the devcontainer
        '''
        self._devcontainer.container_user = container_user
        return self

    def remote_env(self, remote_env_vars: dict[str, str]) -> Self:
        '''
        Specify the per-process environment variables for the container
        '''
        self._devcontainer.remote_env = remote_env_vars
        return self

    def contaniner_env(self, contaniner_env_vars: dict[str, str]) -> Self:
        '''
        Specify the container environment variables for the container
        '''
        self._devcontainer.container_env = contaniner_env_vars
        return self

    def build_spec(self, spec: ContainerBuildSpec) -> Self:
        '''
        Specify the buildspec for the dev container
        '''
        self._devcontainer.build = spec
        return self

    def build_spec_from_args(self, dockerfile: str, context: str, args: dict = None, target: str = None, cache_from: str | list[str] = None) -> Self:
        '''
        Specify the buildspec for the dev container by providing arguments directly
        '''
        self._devcontainer.build = ContainerBuildSpec(
            dockerfile, context, args, target, cache_from)
        return self

    def forwarded_ports(self, ports: list[int]) -> Self:
        '''
        Specify the list of ports to be forwarded from the container
        '''
        self._devcontainer.forward_ports = ports

    def override_command(self, override: bool) -> Self:
        '''
        Specify whether to override the docker image command when starting the dev container
        '''
        self._devcontainer.override_command = override
        return self

    def privileged(self, privileged: bool) -> Self:
        '''
        Specify whether the container will start in privileged mode
        '''
        self._devcontainer.privileged = privileged
        return self

    def security_opts(self, options: list[str]) -> Self:
        '''
        Specify the list of security lables to be applied on the dev container
        '''
        self._devcontainer.security_opt = options

    def capabilities(self, caps: list[str]) -> Self:
        '''
        Specify the list of capabilities for the container
        '''
        self._devcontainer.cap_add = caps

    def mounts(self, mount_list: list[MountSpec]) -> Self:
        '''
        Specify the list of volume mounts to map inside the container
        '''
        if not self._devcontainer.mounts:
            self._devcontainer.mounts = []

        for mount_spec in mount_list:
            self._devcontainer.mounts.append(mount_spec)

        return self

    def workspace_mount(self, mount: str) -> Self:
        '''
        Specify the mount path of the workspace inside the container
        '''
        self._devcontainer.workspace_mount = mount
        return self

    def workspace_folder(self, folder: str) -> Self:
        '''
        Specify the working directory path of the workspace inside the container
        '''
        self._devcontainer.workspace_folder = folder
        return self

    def run_args(self, args: list[str]) -> Self:
        '''
        Specify the additional arguments required during the run
        '''
        self._devcontainer.run_args = args

    def build(self) -> DevContainer:
        '''
        Return the constructed `DevContainer` instance
        '''
        return self._devcontainer
