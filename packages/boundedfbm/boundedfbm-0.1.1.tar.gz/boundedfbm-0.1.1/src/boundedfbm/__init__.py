"""
Bounded FBM Simulator
=====================

A package for simulating bounded Fractional Brownian Motion (FBM)
within 3D shapes created with PyVista.

This package provides tools for:
- Creating various 3D cell shapes using PyVista
- Simulating FBM with time-varying diffusion coefficients
- Modeling Hurst exponents as a Markov chain
- Handling boundary conditions for accurate confinement

Main Components:
---------------
- Cell creation utilities
- FBM simulation with boundary handling
- Markov chain state transitions
- Parameter validation

GitHub: https://github.com/joemans3/boundedfbm
Pypi: https://pypi.org/project/boundedfbm/
    - pip install AMS_BP
Author: Baljyot Singh Parmar
"""

from .cells import CellType, create_cell
from .cells.base_cell import BaseCell
from .motion.FBM import FBM_BP

__version__ = "0.1.1"
# Define public API
__all__ = [
    "__version__",
    "create_cell",
    "CellType",
    "BaseCell",
    "FBM_BP",
]
