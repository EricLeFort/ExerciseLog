import os
import unittest
from importlib import import_module
from typing import List

SEP = os.path.sep
PY_EXT = ".py"
MOD_SEP = "."
INIT = "__init__"
MODULE_PATH = os.path.abspath(os.path.join("..", "src")) + SEP


# TODO these two functions are pretty useful, relocate them to a more re-usable location
def get_files_in_path(path: str) -> List[str]:
    dirs, files = [], []
    for node in os.scandir(path):
        if node.is_dir(follow_symlinks=False):
            dirs.append(node)
        else:
            files.append(node.path)
    return files + [file for dir in dirs for file in get_files_in_path(dir)]


def get_python_files_in_path(path: str) -> List[str]:
    return [f[len(path):] for f in get_files_in_path(path) if f.endswith(PY_EXT)]


class PackageTest(unittest.TestCase):
    def test_import_all_local_modules(self):
        """Simply import every python module under src and verify there's no errors."""
        files = get_python_files_in_path(MODULE_PATH)
        # Strip the ".py" and convert from file paths to python paths
        modules = [f[:-len(PY_EXT)].replace(SEP, MOD_SEP) for f in files]
        # Get rid of the ".__init__" portions
        modules = [module[:-len(INIT) - 1] if module.endswith(INIT) else module for module in modules]
        print(f"Attempting to import the following modules: {modules}")
        [import_module(module) for module in modules]
