'''
Project scaffold generator for Python projects
'''

import os
from copy import deepcopy
from shutil import copytree, move

import jinja2 as j2

from ._generator import ProjectMetadata, ScaffoldGenerator
