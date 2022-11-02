'''
Project data holder
'''

from dataclasses import dataclass


@dataclass(slots=True, init=True)
class ProjectMetadata:
    '''
    Common project metadata
    '''
    project_name: str
    version: str
    project_root: str
