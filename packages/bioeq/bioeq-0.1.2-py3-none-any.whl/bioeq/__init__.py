from importlib import metadata

try:
    __version__ = metadata.version("bioeq")
except metadata.PackageNotFoundError:
    __version__ = "unknown"

from .crossover2x2 import Crossover2x2
from .parallel import ParallelDesign

__all__ = ["Crossover2x2", "ParallelDesign"]
