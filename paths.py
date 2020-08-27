import pathlib

__root_path__ = pathlib.Path(__file__).parent


def get_path(relative_path: str) -> pathlib.Path:
    """Utility to retrieve correct path to asset given a relative path to the root of the project directory"""
    return __root_path__.joinpath(relative_path)
