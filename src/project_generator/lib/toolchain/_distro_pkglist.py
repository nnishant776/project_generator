'''
Module containing definition of package names mapped to specific distribution
for any given toolchain
'''

_toolchain_packages = {
    'rhel': {
        'c': [
            'gcc',
            'gdb',
            '@C Development Tools and Libraries',
        ],
        'cpp': [
            'gcc-c++',
            'clang',
            'llvm',
            'clang-tools-extra',
            'lldb',
            'lld',
        ],
        'gtk': [
            'gtk4-devel',
            'graphene-devel',
            'appstream',
            'appstream-data',
            'appstream-compose',
            'libappstream-glib',
            'desktop-file-utils',
        ],
        'base': [
            'ncurses',
            'nss',
            'unzip',
            'tree',
            'tar',
            'bzip2',
            'zstd',
            'git',
            'curl',
            'wget',
            'vim',
            'python3-pip',
        ],
        'rust': [],
        'go': [],
        'python': [
            'python3-pip',
            'python3-devel',
        ],
    },
    'debian': {
        'c': [
            'gcc',
            'gdb',
            'build-essential'
        ],
        'cpp': [
            'g++',
            'clang',
            'clangd',
            'clang-format',
            'clang-tidy',
            'llvm',
            'lldb',
            'lld',
        ],
        'gtk': [
            'libgtk-4-dev',
            'libgraphene-1.0-dev',
            'appstream',
            'appstream-compose',
            'libappstream-glib-dev',
            'desktop-file-utils',
        ],
        'base': [
            'libncurses6',
            'libnss3',
            'unzip',
            'tree',
            'tar',
            'bzip2',
            'zstd',
            'git',
            'curl',
            'wget',
            'vim',
            'python3-pip',
        ],
        'rust': [],
        'go': [],
        'python': [
            'python3-pip',
            'python3-dev',
        ],
    },
    'arch': {
        'c': [
            'base-devel',
            'gcc',
        ],
        'cpp': [
            'clang',
            'clang-tools-extra',
            'llvm',
            'lldb',
            'lld',
        ],
        'gtk': [
            'gtk4',
            'graphene',
            'appstream',
            'appstream-generator',
            'desktop-file-utils',
        ],
        'base': [
            'ncurses',
            'nss',
            'unzip',
            'tree',
            'tar',
            'bzip2',
            'zstd',
            'git',
            'curl',
            'wget',
            'vim',
            'python3-pip',
        ],
        'rust': [],
        'go': [],
        'python': [
            'python3-pip',
        ],
    },
    'suse': {
        'c': [],
        'cpp': [],
        'gtk': [],
        'base': [],
        'rust': [],
        'go': [],
        'python': [],
    }
}
