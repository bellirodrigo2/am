"""A simple plugin loader."""

import importlib
import os
from collections.abc import Iterable, Sequence


# TODO adicionar includes e excludes
def filter_list(includes: Iterable[str] | None, excludes: Iterable[str] | None):
    pass


def load_all_plugins(path: str, tgt_folder: str) -> None:
    """Loads the plugins defined in the plugins list."""

    def get_plugins(path: str, tgt_folder: str) -> Sequence[str]:
        """Get the python files from parent 'plugin' folder."""

        def read_all_files(path: str, tgt_folder: str) -> Iterable[str]:
            return list(next(os.walk(f"{path}/{tgt_folder}"), (None, None, []))[2])

        walk_list: Iterable[str] = read_all_files(path, tgt_folder)

        def file_to_module_name(file: str, tgt_folder: str) -> str:
            return f"{tgt_folder}.{file}".replace(".py", "")

        return [
            file_to_module_name(x, tgt_folder)
            for x in walk_list
            if x.endswith(".py") and x.startswith("__init__") is False
        ]

    plugins = get_plugins(path, tgt_folder)
    assert len(plugins) > 0, "No Plugins loaded"

    def import_module(name: str):
        """Imports a module given a name."""
        return importlib.import_module(f"{__package__}.{name}")

    for plugin_file in plugins:
        import_module(plugin_file)
