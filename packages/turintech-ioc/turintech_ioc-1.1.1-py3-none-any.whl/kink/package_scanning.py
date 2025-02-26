import ast
import glob
import importlib
import importlib.util
import sys
from _ast import expr
from collections import namedtuple
from pathlib import Path
from typing import AnyStr, List

from kink import inject


def scan():
    """
    Scan decorator to allow decorated classes/functions to populate the dependency injection container in a dynamic way,
    patching the module structure based on the scanning packages provided.
    """
    raise NotImplementedError()


class PackageScanner:
    """
    Implements the logic needed to scan components decorated with @inject, so they can be provided dynamically without
    the need to import them specifically in the places where they need/want to be used.
    """

    import_targets: namedtuple = namedtuple("Import", ["module", "name", "alias"])
    inject_decorator_module: str = inject.__module__

    def _get_imports(self, path):
        with open(path) as fh:
            root = ast.parse(fh.read(), path)

        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.Import):
                module = []
            elif isinstance(node, ast.ImportFrom):
                module = node.module.split(".")
            else:
                continue

            for n in node.names:
                yield self.import_targets(module, n.name.split("."), n.asname)

    def _determine_module_name(self, file_path: Path) -> str:
        """Climbs all parent directories until the parents get exhausted without a match or we hit one of the PYTHONPATH
        entries in order to support namespaced packages (modules with folder without a __init__.py).

        Args:
            file_path: path of the file to produce the module name for.
        Returns:
            module_name: str

        """
        if not file_path.exists():
            raise ValueError("Invalid file path, path does not exist.")

        root_paths: list[str] = sys.path
        i: int = 0
        elements: List[str] = [file_path.name.replace(".py", "")]
        while (
            i < len(file_path.parents)
            and file_path.parents[i].is_dir()
            and str(file_path.parents[i].absolute().resolve()) not in root_paths
        ):
            elements.append(file_path.absolute().parents[i].resolve().name)
            i = i + 1
        return ".".join(reversed(elements))

    def perform_package_scanning(self, pattern: str, base_dir: Path = None):
        """Performs detection of @inject decorated elements (classes) on files listed by the glob matcher.

        On detected classes, it performs dynamic module patching into the imported modules, so dependency injection
        is performed on the fly, adding such components into the dependency injection container for usage later on
        as requested by application elements.
        Args:
            pattern: str: Glob patter to match files against.
            base_dir: Path: base file, provided as an anchor to where apply the glob pattern (if provided).

        """
        elements: List[AnyStr]
        if base_dir is not None:
            if base_dir.is_dir() is False:
                raise ValueError("base_dir argument needs to be a directory.")
            elements = glob.glob(str(base_dir / pattern))
        else:
            elements = glob.glob(pattern, recursive=True)

        for filename in elements:
            with open(filename) as file:
                print(f"Detected file: {filename}")
                node = ast.parse(file.read())
                classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
                for class_ in classes:
                    decorators: list[expr] = class_.decorator_list
                    decorator_names: list[str] = []
                    for deco in decorators:
                        if type(deco) is not ast.Name:
                            decorator_names.append(deco.func.id)
                        else:
                            decorator_names.append(deco.id)
                    if self.inject_decorator_module.split(".")[-1] in decorator_names:
                        if self.inject_decorator_module in [
                            ".".join(module.module + module.name) for module in self._get_imports(filename)
                        ]:
                            module_to_load: str = self._determine_module_name(Path(filename))
                            mod = importlib.import_module(module_to_load)
                            globals().update(mod.__dict__)
                            globals()[mod.__name__] = mod
