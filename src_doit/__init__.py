from pathlib import Path

from hat.doit import common
from hat.doit.py import (get_py_versions,
                         build_wheel,
                         run_pytest,
                         run_flake8)

from .sqlite3 import *  # NOQA
from . import sqlite3


__all__ = ['task_clean_all',
           'task_build',
           'task_check',
           'task_test',
           *sqlite3.__all__]


build_dir = Path('build')
src_py_dir = Path('src_py')
pytest_dir = Path('test_pytest')

build_py_dir = build_dir / 'py'


def task_clean_all():
    """Clean all"""
    return {'actions': [(common.rm_rf, [
        build_dir,
        *(src_py_dir / 'hat/sqlite3').glob('_sqlite3.*')])]}


def task_build():
    """Build"""

    def build():
        build_wheel(
            src_dir=src_py_dir,
            dst_dir=build_py_dir,
            name='hat-sqlite3',
            description='Hat Sqlite3 build',
            url='https://github.com/hat-open/hat-sqlite3',
            license=common.License.APACHE2,
            py_versions=get_py_versions(None),
            platform=common.target_platform,
            has_ext_modules=True)

    return {'actions': [build],
            'task_dep': ['sqlite3']}


def task_check():
    """Check with flake8"""
    return {'actions': [(run_flake8, [src_py_dir]),
                        (run_flake8, [pytest_dir])]}


def task_test():
    """Test"""
    return {'actions': [lambda args: run_pytest(pytest_dir, *(args or []))],
            'pos_arg': 'args',
            'task_dep': ['sqlite3']}
