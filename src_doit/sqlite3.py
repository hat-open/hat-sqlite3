from pathlib import Path

from hat.doit import common
from hat.doit.c import (get_target_ext_suffix,
                        get_py_cpp_flags,
                        get_py_ld_flags,
                        CBuild)


__all__ = ['task_sqlite3',
           'task_sqlite3_obj',
           'task_sqlite3_dep',
           'task_sqlite3_cleanup']


build_dir = Path('build')
src_c_dir = Path('src_c')
src_py_dir = Path('src_py')

target_ext_suffix = get_target_ext_suffix(None)
sqlite3_path = src_py_dir / f'hat/sqlite3/_sqlite3{target_ext_suffix}'


def task_sqlite3():
    """Build sqlite3"""
    return _build.get_task_lib(sqlite3_path)


def task_sqlite3_obj():
    """Build sqlite3 .o files"""
    yield from _build.get_task_objs()


def task_sqlite3_dep():
    """Build sqlite3 .d files"""
    yield from _build.get_task_deps()


def task_sqlite3_cleanup():
    """Cleanup sqlite3"""
    return {'actions': [_cleanup]}


def _cleanup():
    for path in sqlite3_path.parent.glob('_sqlite3.*'):
        if path == sqlite3_path:
            continue
        common.rm_rf(path)


def _get_cpp_flags():
    yield from get_py_cpp_flags(None)
    yield '-DMODULE_NAME="_sqlite3"'
    yield f"-I{src_c_dir / 'sqlite3'}"


def _get_cc_flags():
    yield '-fPIC'
    yield '-O2'
    yield '-Wno-return-local-addr'


def _get_ld_flags():
    yield from get_py_ld_flags(None)


_build = CBuild(
    src_paths=[*(src_c_dir / 'sqlite3').rglob('*.c'),
               *(src_c_dir / 'py/_sqlite3').rglob('*.c')],
    build_dir=(build_dir / 'sqlite3' /
                           f'{common.target_platform.name.lower()}_'
                           f'{common.target_py_version.name.lower()}'),
    cpp_flags=list(_get_cpp_flags()),
    cc_flags=list(_get_cc_flags()),
    ld_flags=list(_get_ld_flags()),
    task_dep=['sqlite3_cleanup'])
