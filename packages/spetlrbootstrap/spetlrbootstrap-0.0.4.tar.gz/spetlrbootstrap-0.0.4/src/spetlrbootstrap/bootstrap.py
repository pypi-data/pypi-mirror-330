import glob
import importlib

from pip._internal.cli.main import main as pip_main

from spetlrbootstrap.arguments import DEPENDENCIES, ENTRY_POINT, LIBRARY, unpack_argv
from spetlrbootstrap.introspect_entrypoint import prepare_keyword_arguments


def bootstrap():
    """This function is an entry point from which another entry point can be called.
    If you want to call this function:
    ```python
        def myfunction(myarg='default'): pass
    ```
    that is residing in the folder `mylib.myfolder.myfile`,
    then specify your task as follows:
    ```json
        "python_wheel_task": {
            "package_name": "spetlrbootstrap",
            "entry_point": "spetlrbootstrap",
            "named_parameters": {
                "library": "/Volumes/path/to/my/library.whl",
                "dependencies": "/Volumes/path/to/my/dependencies/*.whl",
                "entry_point": "mylib.myfolder.myfile:myfunction",
                "myarg": "myval"
            }
        }
    ```
    The named parameter 'entry_point' is mandatory, 'library' and 'dependencies' are optional.
    All arguments must be of type string.
    """

    params = unpack_argv()

    entry_point = params.pop(ENTRY_POINT)
    library = params.pop(LIBRARY, None)
    dependencies = params.pop(DEPENDENCIES, None)

    toinstall = []
    if library:
        toinstall.append(library)
    if dependencies:
        toinstall.extend(glob.glob(dependencies))
    if toinstall:
        print("Installing dependencies...")
        pip_main(["install", "--no-deps"] + toinstall)
        print("Installing dependencies done.")

    # entry_point looks like "my.module:main"
    modname, qualname_separator, qualname = entry_point.partition(":")

    obj = importlib.import_module(modname)
    if qualname_separator:
        for attr in qualname.split("."):
            obj = getattr(obj, attr)

    kwargs = prepare_keyword_arguments(obj, params)

    # call the callable with custom parameters
    return obj(**kwargs)
