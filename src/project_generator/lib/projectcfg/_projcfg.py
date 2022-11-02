'''
Module dealing with project configuration based on the selected template
'''

from enum import Enum
from dataclasses import dataclass
from copy import deepcopy

from typing_extensions import Self

from project_generator.lib.devenvcfg import devcontainer


class ProjectTemplate(Enum):
    '''
    An enumeration listing all the supported project templates
    '''
    C = 'c'
    CPP = 'cpp'
    RUST = 'rust'
    GO = 'go'
    PYTHON = 'python'


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


@dataclass(slots=True)
class ProjectConfig:
    '''
    Holds the project configuration which is defined based on the user input
    '''
    project_template: ProjectTemplate = None
    required_toolchains: list[Toolchain] = None
    enable_debug_support: bool = True
    devcontainer_cfg: devcontainer.DevContainer = None
    editor_cfg = None

    def debug_enabled(self) -> bool:
        '''
        Check whether debug support is enabled
        '''
        return self.enable_debug_support

    def template(self) -> ProjectTemplate:
        '''
        Get the project template
        '''
        return self.project_template

    def toolchains(self) -> list[Toolchain]:
        '''
        Get the list of required toolchains
        '''
        return self.required_toolchains

    def devcontainer_config(self) -> devcontainer.DevContainer:
        '''
        Get the devcontainer configuration
        '''
        return self.devcontainer_cfg

    def editor_config(self):
        '''
        Get the editor configuration
        '''
        return self.editor_cfg


@dataclass(slots=True)
class ProjectConfigBuilder:
    '''
    A helper class to construct project configuration metadata
    '''
    _projcfg: ProjectConfig

    def __init__(self):
        self._projcfg = ProjectConfig()

    def template(self, template: ProjectTemplate) -> Self:
        '''
        Specify the project template
        '''
        self._projcfg.project_template = template
        return self

    def enable_debug(self, debug_support: bool = True) -> Self:
        '''
        Specify whether to enable debugging for the project
        '''
        self._projcfg.enable_debug_support = debug_support
        return self

    def extra_toolchains(self, toolchains: list[Toolchain]) -> Self:
        '''
        Specify the addtional toolchains to be installed
        '''
        if self._projcfg.required_toolchains is None:
            self._projcfg.required_toolchains = deepcopy(toolchains)
        else:
            for tlchn in toolchains:
                self._projcfg.required_toolchains.append(tlchn)
        return self

    def devcontaier_config(self, dev_cnt_cfg: devcontainer.DevContainer) -> Self:
        '''
        Specify a devcontainer configuration to use with the project
        '''
        self._projcfg.devcontainer_cfg = deepcopy(dev_cnt_cfg)
        return self

    def editor_config(self, editor_cfg) -> Self:
        '''
        Specify an editor configuration to use with the project
        '''
        self._projcfg.editor_cfg = deepcopy(editor_cfg)
        return self
