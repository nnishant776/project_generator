'''
Test module for project scaffold generator
'''

import os
import unittest

from project_generator.lib.projectcfg import ProjectTemplate
from project_generator.lib.scaffold import ProjectScaffoldBuilder


class TestScaffold(unittest.TestCase):
    '''
    Test suite for testing scaffold generation
    '''

    def test_c_projgen(self):
        '''
        Test C project generation
        '''
        scaffold_builder = ProjectScaffoldBuilder().project_name(
            'arknights-c').version("0.2.1").template(ProjectTemplate.C).build()
        scaffold_builder.build_scaffold()
        self.assertEqual(os.path.exists('arknights-c'), True)

    def test_cpp_projgen(self):
        '''
        Test C++ project generation
        '''
        scaffold_builder = ProjectScaffoldBuilder().project_name(
            'arknights-cpp').version("0.2.1").template(ProjectTemplate.CPP).build()
        scaffold_builder.build_scaffold()
        self.assertEqual(os.path.exists('arknights-cpp'), True)

    def test_rust_projgen(self):
        '''
        Test Rust project generation
        '''
        scaffold_builder = ProjectScaffoldBuilder().project_name(
            'arknights-rs').version("0.1.0").template(ProjectTemplate.RUST).build()
        scaffold_builder.build_scaffold()
        self.assertEqual(os.path.exists('arknights-rs'), True)

    def test_go_projgen(self):
        '''
        Test Go project generation
        '''
        scaffold_builder = ProjectScaffoldBuilder().project_name(
            'arknights-go').version("0.1.0").template(ProjectTemplate.GO).build()
        scaffold_builder.build_scaffold()
        self.assertEqual(os.path.exists('arknights-go'), True)


if __name__ == '__main__':
    unittest.main()
