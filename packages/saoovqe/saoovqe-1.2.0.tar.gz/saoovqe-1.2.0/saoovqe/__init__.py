"""Init file for module saoovqe.

This file imports everything from the project to prove
all-encompassing interface.
"""

from pathlib import Path
import importlib.metadata
import tomllib

__version__ = None

try:
    __version__ = importlib.metadata.version('saoovqe')
except importlib.metadata.PackageNotFoundError:
    __version__ = tomllib.load(open(f'{Path(__file__).parent.parent}/pyproject.toml', 'rb'))['project']['version']

try:
    import psi4
except ImportError:
    raise ImportError('Psi4 is required but not installed. '
                      'Please install it manually: https://psicode.org/psi4manual/master/build_obtaining.html')

import qiskit_nature
from .ansatz import *
from .circuits import *
from .gradient import *
from .logger_config import *
from .problem import *
from .vqe_optimization import *

##################
# Global Settings
##################
qiskit_nature.settings.dict_aux_operators = True
