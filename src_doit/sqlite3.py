from pathlib import Path

import sysconfig

from hat.doit import common
from hat.doit.c import (target_ext_suffix,
                        CBuild)


__all__ = ['task_sqlite3',
           'task_sqlite3_obj',
           'task_sqlite3_dep',
           'task_sqlite3_cleanup']


build_dir = Path('build')
src_c_dir = Path('src_c')
src_py_dir = Path('src_py')

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
    _, major, minor = common.target_py_version.value

    if common.target_platform == common.local_platform:
        if common.target_py_version == common.local_py_version:
            include_path = sysconfig.get_path('include')
            if include_path:
                yield f'-I{include_path}'

        elif common.local_platform == common.Platform.LINUX:
            yield f'-I/usr/include/python{major}.{minor}'

        else:
            raise ValueError('unsupported version')

    elif (common.local_platform, common.target_platform) == (
            common.Platform.LINUX, common.Platform.WINDOWS):
        yield f'-I/usr/x86_64-w64-mingw32/include/python{major}{minor}'

    else:
        raise ValueError('unsupported platform')

    yield '-DMODULE_NAME="_sqlite3"'
    yield f"-I{src_c_dir / 'sqlite3'}"


def _get_cc_flags():
    yield '-fPIC'
    yield '-O2'
    yield '-Wno-return-local-addr'


def _get_ld_flags():
    _, major, minor = common.target_py_version.value

    if common.target_platform == common.local_platform:
        if common.local_platform == common.Platform.DARWIN:
            stdlib_path = (Path(sysconfig.get_path('stdlib')) /
                           f'config-{major}.{minor}-darwin')
            yield f"-L{stdlib_path}"

        elif common.local_platform == common.Platform.WINDOWS:
            data_path = sysconfig.get_path('data')
            yield f"-L{data_path}"

    if common.target_platform == common.Platform.WINDOWS:
        yield f"-lpython{major}{minor}"

    else:
        yield f"-lpython{major}.{minor}"


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
