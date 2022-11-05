from enum import Enum


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
