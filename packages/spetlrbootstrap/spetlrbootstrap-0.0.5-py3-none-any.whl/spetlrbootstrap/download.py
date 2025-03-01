import json
import os
import sys
from pathlib import Path

from pip._internal.cli.main import main as pip_main

from spetlrbootstrap.arguments import DEPENDENCIES, REQUIREMENTS, unpack_argv
from spetlrbootstrap.libraries import list_all_libs


def download():
    params = unpack_argv()
    dependencies = params.pop(DEPENDENCIES)
    raw_requirements = params.pop(REQUIREMENTS)
    requirements = [r.strip() for r in json.loads(raw_requirements) if r.strip()]

    if "*" in dependencies:
        dependencies = str(Path(dependencies).parent)

    print("Specified requirements:")
    for r in requirements:
        print(" -", r)
    print()
    print("Specified download directory:")
    print(dependencies)
    print()

    print("Now establishing baseline packages that are already installed.")
    print("The will not be downloaded in dependencies folder.")
    default_libs = list_all_libs()

    print("Ensuring download destination exists...")
    Path(dependencies).mkdir(parents=True, exist_ok=True)

    print("Ensuring that specified download directory is empty...")
    if len(os.listdir(dependencies)) != 0:
        print("ERROR: the download directory is not empty.")
        sys.exit(1)

    pip_main(["install", "--no-deps"] + requirements)

    all_libs = list_all_libs()
    lib_dependencies = all_libs - default_libs

    print("Identified packages for download:")
    for lib in lib_dependencies:
        print("  ", lib)

    if not lib_dependencies:
        print("ERROR: No packages for download.")
        sys.exit(1)

    print("Now downloading all from pypi...")

    os.chdir(dependencies)
    pip_main(["download"] + list(lib_dependencies))

    print("All done.")
