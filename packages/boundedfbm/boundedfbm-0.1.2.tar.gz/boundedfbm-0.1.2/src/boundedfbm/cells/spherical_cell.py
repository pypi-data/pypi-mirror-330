from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pyvista as pv

from .base_cell import BASE_TOLERANCE, BaseCell
from .typedefs import Vector3D


@dataclass
class SphericalCell(BaseCell):
    """
    Represents a spherical cell in 3D space, centered around Z=0.

    Attributes:
        center (Tuple[float,float,float]): center coordinate of the sphere
        radius (float): Radius of the sphere
    """

    center: Tuple[float, float, float]
    radius: float

    def __post_init__(self):
        super().__post_init__() if hasattr(super(), "__post_init__") else None
        # Precalculate values needed for is_point_inside method
        self._setup_containment_check()

    def _setup_containment_check(self):
        """
        Precalculates values needed for efficient point containment checks.
        """
        # Precalculate squared radius for more efficient distance checks
        self._radius_squared = self.radius**2

    def contains_point_fallback(
        self, x: float, y: float, z: float, tolerance: float = BASE_TOLERANCE
    ) -> bool:
        """
        Determines if a point (x, y, z) is inside the spherical cell.

        Args:
            x (float): X-coordinate of the point
            y (float): Y-coordinate of the point
            z (float): Z-coordinate of the point

        Returns:
            bool: True if the point is inside the sphere, False otherwise
        """
        # Calculate squared distance from point to center
        # Using squared distance avoids costly square root operation
        dx = x - self.center[0]
        dy = y - self.center[1]
        dz = z - self.center[2]
        distance_squared = dx * dx + dy * dy + dz * dz

        # Check if the point is within the radius of the sphere
        return distance_squared <= self._radius_squared


def make_SphericalCell(
    center: Tuple[float, float, float], radius: float
) -> SphericalCell:
    return SphericalCell(
        mesh=pv.Sphere(radius=radius, center=center), center=center, radius=radius
    )


@dataclass
class SphericalCellParams:
    center: Vector3D
    radius: float

    @classmethod
    def validate_center(cls, value):
        if not isinstance(value, (list, tuple, np.ndarray)) or len(value) != 3:
            raise ValueError("center must be a 3D vector")

    @classmethod
    def validate_radius(cls, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("radius must be a positive number")
