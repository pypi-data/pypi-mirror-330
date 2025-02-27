# coding=utf-8


import sys
import os.path
import importlib.util  # @ exp | For lsp, or juts import importlib
import inspect

from . import EasyArg


def load_module_from_path(module_path, module_name=None):
    """
    load a module from filepath
    -----------------------------------
    Last Update: 2024-04-12
    """
    if module_name is None:
        module_name = module_path.split('/')[-1].split('.')[0]

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    if len(sys.argv) < 3 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print("Usage: pyfexe [-h, --help] your-script your-func [-h, --help] [arguments]")
        sys.exit(0)

    assert os.path.exists(sys.argv[1]) and sys.argv[1].endswith(".py"), f"Not valid script: {sys.argv[1]}"

    ea = EasyArg()

    M = load_module_from_path(sys.argv[1])
    if sys.argv[2] == "-h" or sys.argv[2] == "--help":
        for name, obj in inspect.getmembers(M, inspect.isfunction):
            if obj.__module__ == M.__name__:
                try:
                    ea.command()(obj)
                except:
                    ea.parser.remove_subparser(name)

        ea.parser.print_help()
        sys.exit(0)
    assert hasattr(M, sys.argv[2])

    func = getattr(M, sys.argv[2])

    ea.command()(func)
    ea.parse(sys.argv[2:])


if __name__ == "__main__":
    main()
