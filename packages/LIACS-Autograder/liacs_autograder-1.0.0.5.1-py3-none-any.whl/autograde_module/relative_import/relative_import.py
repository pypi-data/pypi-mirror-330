import pathlib
import importlib

# Credits towards imptools: https://github.com/danijar/imptools/blob/main/imptools/enable_relative.py

def enable_relative():
    import __main__

    # Skip if the script is executed as a module.
    if __main__.__package__ is not None:
        return

    # Skip if running from interactive interpreter.
    if not hasattr(__main__, '__file__'):
        return

    # Find the top level module that __main__ is part of
    root = pathlib.Path(__main__.__file__).parent
    toplevel_package = root.name
    while (root.parent / "__init__.py").is_file():  # If the parent directory has no __init__.py the top level has been found
        root = root.parent
        toplevel_package = root.name + "." + toplevel_package
    __main__.__package__ = toplevel_package
