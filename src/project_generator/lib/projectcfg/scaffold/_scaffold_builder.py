'''
Helper module to create a project scaffold
'''

import os
from dataclasses import dataclass

from typing_extensions import Self

from .._projcfg import ProjectTemplate
from ._generator import (CppScaffoldGenerator, CScaffoldGenerator,
                         GoScaffoldGenerator, RustScaffoldGenerator,
                         ScaffoldGenerator)


@dataclass(slots=True)
class ProjectScaffoldBuilder:
    '''
    Helper class to construct a project scaffold
    '''
    _project_name: str = ""
    _version: str = ""
    _project_root: str = ""
    _template: ProjectTemplate = None
    _project_scaffold: ScaffoldGenerator = None

    def project_name(self, name: str) -> Self:
        '''
        Specify the project name
        '''
        if name == "":
            raise ValueError("empty project name")

        self._project_name = name
        return self

    def version(self, version: str) -> Self:
        '''
        Specify the project version
        '''
        self._version = version
        return self

    def template(self, project_template: ProjectTemplate) -> Self:
        '''
        Specify the project template to use
        '''
        if project_template is None:
            raise ValueError(f"invalid project template {project_template}")

        self._template = project_template
        return self

    def root_dir(self, root_dir: str) -> Self:
        '''
        Specify the root director to build the scaffold in. Note that this WILL
        create a top level project directory if it doesn't already exist. If
        root directory is not specified, the application will create the scaffold
        in current directory.
        '''
        if root_dir == "":
            root_dir = os.getcwd()
        self._project_root = root_dir
        return self

    def build(self) -> ScaffoldGenerator:
        '''
        Return the constructed scaffold generator
        '''

        if self._template == ProjectTemplate.C:
            self._project_scaffold = CScaffoldGenerator(
                self._project_name, self._version, self._project_root)
        elif self._template == ProjectTemplate.CPP:
            self._project_scaffold = CppScaffoldGenerator(
                self._project_name, self._version, self._project_root)
        elif self._template == ProjectTemplate.RUST:
            self._project_scaffold = RustScaffoldGenerator(
                self._project_name, self._version, self._project_root)
        elif self._template == ProjectTemplate.GO:
            self._project_scaffold = GoScaffoldGenerator(
                self._project_name, self._version, self._project_root)

        return self._project_scaffold
