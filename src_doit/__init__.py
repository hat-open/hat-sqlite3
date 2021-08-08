from pathlib import Path

from hat.doit import common

from .sqlite3 import *  # NOQA
from . import sqlite3


__all__ = ['task_clean_all',
           'task_build',
           *sqlite3.__all__]


build_dir = Path('build')
src_py_dir = Path('src_py')


def task_clean_all():
    """Clean all"""
    return {'actions': [(common.rm_rf, [build_dir,
                                        sqlite3.sqlite3_path])]}


def task_build():
    """Build"""

    def build():
        common.wheel_build(
            src_dir=src_py_dir,
            dst_dir=build_dir / 'py',
            src_paths=list(common.path_rglob(src_py_dir,
                                             blacklist={'__pycache__'})),
            name='hat-sqlite3',
            description='Hat Sqlite3 build',
            url='https://github.com/hat-open/hat-sqlite3',
            license=common.License.APACHE2,
            packages=['hat'],
            requirements_path=None,
            platform_specific=True)

    return {'actions': [build],
            'task_dep': ['sqlite3']}
