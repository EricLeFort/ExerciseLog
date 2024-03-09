import os
import unittest
from importlib import import_module
from pathlib import Path

SEP = os.sep
PY_EXT = ".py"
MOD_SEP = "."
INIT = "__init__"
MODULE_PATH = (Path("..") / "src").resolve()


class TestPackage(unittest.TestCase):
    def test_import_all_local_modules(self) -> None:
        """Simply import every python module under src and verify there's no errors."""
        # Recursively find all *.py files in this package's files, remove the suffix, then convert to python modules
        files = [f.with_suffix("").relative_to(MODULE_PATH) for f in MODULE_PATH.glob("**/*.py")]
        modules = [str(f).replace(SEP, MOD_SEP) for f in files]
        # Get rid of the ".__init__" portions
        modules = [module[: -len(INIT) - 1] if module.endswith(INIT) else module for module in modules]
        for module in modules:
            import_module(module)
