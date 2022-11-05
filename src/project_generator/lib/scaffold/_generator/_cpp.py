'''
Project scaffold generator for C++ projects
'''

import os
from dataclasses import dataclass
from tempfile import mkdtemp
from shutil import copytree, move

import jinja2 as j2

from ._generator import ScaffoldGenerator


@dataclass(slots=True, init=True)
class CppScaffoldGenerator(ScaffoldGenerator):
    '''
    Generate C++ project scaffold
    '''

    def build_scaffold(self):
        if self.project_name == "":
            raise ValueError("empty project name not allowed")

        if self.version == "":
            self.version = "0.1.0"

        if self.project_root == "":
            self.project_root = os.getcwd()

        project_path = os.path.join(self.project_root, self.project_name)

        # create a tmeporary directory and copy the templates to it
        temp_eval_path = mkdtemp(suffix="_projgen")
        copytree(f"{os.path.dirname(__file__)}/../_templates/cpp/",
                 temp_eval_path, dirs_exist_ok=True)

        # process the jinja template present in the temporary directory
        # and write them out to their final output files
        environment = j2.Environment(loader=j2.FileSystemLoader(
            f"{temp_eval_path}"))
        renderer = environment.get_template('cpp_meson.build')
        with open(f"{temp_eval_path}/meson.build", "w", encoding="utf-8") as file:
            file.write(renderer.render({
                'project_name': self.project_name,
                'version': self.version
            }))

        # remove the templates from  the temporary directory
        os.remove(f"{temp_eval_path}/cpp_meson.build")

        # make sure the parent directory of the project path exists
        os.makedirs(os.path.dirname(project_path), 0o755, exist_ok=True)

        # move the evaluated template files in the temporary directory to
        # their final destination
        move(temp_eval_path, project_path)
