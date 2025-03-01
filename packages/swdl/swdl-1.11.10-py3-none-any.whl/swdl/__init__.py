from importlib.metadata import version

from .config import Settings

settings = Settings()

__version__ = version("swdl")
