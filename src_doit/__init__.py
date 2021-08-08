from pathlib import Path
import subprocess
import sys

from hat.doit import common

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


def task_check():
    """Check with flake8"""
    return {'actions': [(_run_flake8, [src_py_dir]),
                        (_run_flake8, [pytest_dir])]}


def task_test():
    """Test"""

    def run(args):
        subprocess.run([sys.executable, '-m', 'pytest',
                        '-s', '-p', 'no:cacheprovider',
                        *(args or [])],
                       cwd=str(pytest_dir),
                       check=True)

    return {'actions': [run],
            'pos_arg': 'args',
            'task_dep': ['sqlite3']}


def _run_flake8(path):
    subprocess.run([sys.executable, '-m', 'flake8', str(path)],
                   check=True)
