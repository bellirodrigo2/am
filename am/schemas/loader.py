"""A simple plugin loader."""

import importlib
import os

###############################################################################


def import_module(name: str):
    """Imports a module given a name."""
    return importlib.import_module(f"{__package__}.{name}")


def file_to_module_name(file: str, tgt_folder: str) -> str:
    return f"{tgt_folder}.{file}".replace(".py", "")


def read_all_files(path: str, tgt_folder: str) -> list[str]:
    return list(next(os.walk(f"{path}/{tgt_folder}"), (None, None, []))[2])


def get_plugins(path: str, tgt_folder: str) -> list[str]:
    """Get the python files from parent 'plugin' folder."""

    walk_list: list[str] = read_all_files(path, tgt_folder)

    return [
        file_to_module_name(x, tgt_folder)
        for x in walk_list
        if x.endswith(".py") and x.startswith("__init__") is False
    ]


def filter_list(includes: list[str] | None, excludes: list[str] | None):
    pass


def load_all_plugins(path: str, tgt_folder: str) -> None:
    """Loads the plugins defined in the plugins list."""

    plugins = get_plugins(path, tgt_folder)
    assert len(plugins) > 0, "No Plugins loaded"
    for plugin_file in plugins:
        import_module(plugin_file)
