'''
Module containing definition of package names mapped to specific distribution
for any given toolchain
'''

_toolchain_packages = {
    'rhel': {
        'c': [
            '@C Development Tools and Libraries',
            'clang',
            'lldb',
            'lld',
        ],
        'cpp': [
            'llvm',
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
            'clang',
            'lldb',
            'lld',
            'build-essential',
        ],
        'cpp': [
            'llvm',
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
            'clang',
            'lldb',
            'lld',
        ],
        'cpp': [
            'llvm',
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
            'python-pip',
        ],
        'rust': [],
        'go': [],
        'python': [
            'python-pip',
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

_extra_tools_packages = {
    'rhel': {
        'c': [
            'clang-tools-extra',
            'cmake',
            'make',
            'pkgconf'
        ],
        'cpp': [],
        'gtk': [
            'd-feet'
        ],
        'base': [],
        'rust': [],
        'go': [],
        'python': [],
    },
    'debian': {
        'c': [
            'clangd',
            'cmake',
            'make',
            'pkgconf'
        ],
        'cpp': [],
        'gtk': [
            'd-feet'
        ],
        'base': [],
        'rust': [],
        'go': [],
        'python': [],
    },
    'arch': {
        'c': [
            'clang-tools-extra',
            'cmake',
            'make',
            'pkgconf'
        ],
        'cpp': [],
        'gtk': [
            'd-feet',
        ],
        'base': [],
        'rust': [],
        'go': [],
        'python': [],
    },
    'suse': {
        'c': [],
        'cpp': [],
        'gtk': [],
        'base': [],
        'rust': [],
        'go': [],
        'python': [],
    },
}
