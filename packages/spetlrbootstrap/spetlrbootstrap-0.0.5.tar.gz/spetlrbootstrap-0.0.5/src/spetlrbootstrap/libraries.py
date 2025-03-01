import importlib.metadata


def list_all_libs():
    libs = set()
    for dist in importlib.metadata.distributions():
        libs.add(dist.metadata["Name"])
    return libs
