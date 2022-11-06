
'''
Project scaffold generator for Rust projects
'''

import os
from dataclasses import dataclass
from shutil import copytree, move
from tempfile import mkdtemp

import jinja2 as j2

from ._generator import ScaffoldGenerator


@dataclass(slots=True, init=True)
class RustScaffoldGenerator(ScaffoldGenerator):
    '''
    Generate Rust project scaffold
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
        copytree(f"{os.path.dirname(__file__)}/../_templates/rust/",
                 temp_eval_path, dirs_exist_ok=True)

        # process the jinja template for meson.build present in the temporary
        # directory and write them out to the final output file
        environment = j2.Environment(loader=j2.FileSystemLoader(
            f"{temp_eval_path}"))
        meson_renderer = environment.get_template('rust_meson.build')
        with open(f"{temp_eval_path}/meson.build", "w", encoding="utf-8") as file:
            file.write(meson_renderer.render({
                'project_name': self.project_name,
                'version': self.version
            }))

        # remove the meson.build template from the temporary directory
        os.remove(f"{temp_eval_path}/rust_meson.build")

        # process the jinja template for Cargo.toml present in the temporary
        # directory and write them out to the final output file
        cargo_toml_renderer = environment.get_template('rust_Cargo.toml')
        with open(f"{temp_eval_path}/Cargo.toml", "w", encoding="utf-8") as file:
            file.write(cargo_toml_renderer.render({
                'project_name': self.project_name,
                'version': self.version
            }))

        # remove the Cargo.toml template from the temporary directory
        os.remove(f"{temp_eval_path}/rust_Cargo.toml")

        # move the evaluated template files in the temporary directory to
        # their final destination
        move(temp_eval_path, project_path)
