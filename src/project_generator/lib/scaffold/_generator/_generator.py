from dataclasses import dataclass

from ._project_data import ProjectMetadata


@dataclass(slots=True, init=True)
class ScaffoldGenerator(ProjectMetadata):
    '''
    Base class for all the scaffold generator
    '''

    def build_scaffold(self):
        '''
        Create the project scaffold
        '''
