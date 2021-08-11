from pathlib import Path

import sysconfig
import sys

from hat.doit.c import CBuild


__all__ = ['task_sqlite3',
           'task_sqlite3_obj',
           'task_sqlite3_dep']


build_dir = Path('build')
src_c_dir = Path('src_c')
src_py_dir = Path('src_py')

sqlite3_path = (src_py_dir / 'hat/sqlite3/_sqlite3').with_suffix(
    '.pyd' if sys.platform == 'win32' else '.so')


def task_sqlite3():
    """Build sqlite3"""
    return _build.get_task_lib(sqlite3_path)


def task_sqlite3_obj():
    """Build sqlite3 .o files"""
    yield from _build.get_task_objs()


def task_sqlite3_dep():
    """Build sqlite3 .d files"""
    yield from _build.get_task_deps()


def _get_cpp_flags():
    include_path = sysconfig.get_path('include')

    if sys.platform == 'linux':
        yield f'-I{include_path}'

    elif sys.platform == 'darwin':
        pass

    elif sys.platform == 'win32':
        yield f'-I{include_path}'

    else:
        raise Exception('unsupported platform')

    yield '-DMODULE_NAME="_sqlite3"'
    yield f"-I{src_c_dir / 'sqlite3'}"


def _get_cc_flags():
    yield '-fPIC'
    yield '-O2'
    yield '-Wno-return-local-addr'


def _get_ld_flags():
    if sys.platform == 'linux':
        pass

    elif sys.platform == 'darwin':
        python_version = f'{sys.version_info.major}.{sys.version_info.minor}'
        stdlib_path = (Path(sysconfig.get_path('stdlib')) /
                       f'config-{python_version}-darwin')
        yield f"-L{stdlib_path}"
        yield f"-lpython{python_version}"

    elif sys.platform == 'win32':
        data_path = sysconfig.get_path('data')
        python_version = f'{sys.version_info.major}{sys.version_info.minor}'
        yield f"-L{data_path}"
        yield f"-lpython{python_version}"

    else:
        raise Exception('unsupported platform')


_build = CBuild(
    src_paths=[*(src_c_dir / 'sqlite3').rglob('*.c'),
               *(src_c_dir / 'py/_sqlite3').rglob('*.c')],
    src_dir=src_c_dir,
    build_dir=build_dir / 'sqlite3',
    cpp_flags=list(_get_cpp_flags()),
    cc_flags=list(_get_cc_flags()),
    ld_flags=list(_get_ld_flags()))
