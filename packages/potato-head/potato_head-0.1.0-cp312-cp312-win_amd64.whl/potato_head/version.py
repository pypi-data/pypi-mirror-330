from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("potato_head")
except PackageNotFoundError:
    __version__ = "unknown"
