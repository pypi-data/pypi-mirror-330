from contextlib import contextmanager
import os
import shutil
import tempfile
from pathlib import Path

from .hmd_cli_tools import cd


@contextmanager
def build_dir(repo_name: str = None):
    cwd = os.getcwd()
    if repo_name is None:
        repo_name = cwd.split(os.sep)[-1]

    cwd_path = Path(cwd)
    tmpdir = tempfile.gettempdir()

    if cwd_path.is_relative_to(tmpdir):
        yield
    else:
        tmp_dir = tempfile.gettempdir()
        build_dir = Path(tmp_dir) / repo_name
        if not os.path.exists(build_dir):
            shutil.copytree(cwd, build_dir)
        with cd(build_dir):
            yield
