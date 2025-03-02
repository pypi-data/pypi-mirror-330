from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pyvista as pv
from typing_extensions import List

from .base_cell import BASE_TOLERANCE, BaseCell
from .typedefs import Vector3D


@dataclass
class RodCell(BaseCell):
    """
    Represents a rod-like cell in 3D space.

    Attributes:
        center (np.ndarray): The (x, y, z) coordinates of the cell's center in XYZ plane
        direction (np.ndarray): direction vector of the orientation of the RodCell
        height (float): length of the rod, NOT including end caps
        radius (float): Radius of both the cylindrical body and hemispheres

        +

        pyvista mesh for the BaseCell
    """

    center: np.ndarray | List[float] | Tuple
    direction: np.ndarray | List[float] | Tuple
    height: float
    radius: float

    def __post_init__(self):
        super().__post_init__() if hasattr(super(), "__post_init__") else None
        # Convert lists/tuples to numpy arrays if necessary
        if not isinstance(self.center, np.ndarray):
            self.center = np.array(self.center, dtype=float)
        if not isinstance(self.direction, np.ndarray):
            self.direction = np.array(self.direction, dtype=float)

        # Precalculate values needed for point containment checks
        self._setup_containment_check()

    def _setup_containment_check(self):
        """
        Precalculates values needed for efficient point containment checks.
        """
        # Normalize the direction vector
        self._direction_norm = self.direction / np.linalg.norm(self.direction)

        # Calculate half-height for cylinder bounds checking
        self._half_height = self.height / 2

        # Precalculate squared radius for more efficient distance checks
        self._radius_squared = self.radius**2

        # Calculate cylinder end points (centers of the hemispheres)
        self._end1 = self.center + self._direction_norm * self._half_height
        self._end2 = self.center - self._direction_norm * self._half_height

    def contains_point_fallback(
        self, x: float, y: float, z: float, tolerance: float = BASE_TOLERANCE
    ) -> bool:
        """
        Determines if a point (x, y, z) is inside the rod cell.
        A rod cell consists of a cylinder with hemispherical caps at both ends.

        Args:
            x (float): X-coordinate of the point
            y (float): Y-coordinate of the point
            z (float): Z-coordinate of the point

        Returns:
            bool: True if the point is inside the rod cell, False otherwise
        """
        # Convert point to numpy array
        point = np.array([x, y, z])

        # Vector from center to the point
        center_to_point = point - self.center

        # Project the vector onto the rod's axis
        projection_length = np.dot(center_to_point, self._direction_norm)

        # CASE 1: Point is near the cylindrical part of the rod
        if abs(projection_length) <= self._half_height:
            # Calculate the distance from the point to the rod's axis
            # This is the distance from the point to the line through the center along direction
            # Formula: |v - (v·d)d| where v is vector from center to point and d is direction
            distance_to_axis_squared = np.sum(
                (center_to_point - projection_length * self._direction_norm) ** 2
            )

            # Check if the point is within the radius of the cylinder
            return distance_to_axis_squared <= self._radius_squared

        # CASE 2 & 3: Point is near one of the hemispherical caps
        elif projection_length > self._half_height:
            # Point is near the positive direction cap
            distance_to_cap_center_squared = np.sum((point - self._end1) ** 2)
            return distance_to_cap_center_squared <= self._radius_squared

        else:  # projection_length < -self._half_height
            # Point is near the negative direction cap
            distance_to_cap_center_squared = np.sum((point - self._end2) ** 2)
            return distance_to_cap_center_squared <= self._radius_squared


def make_RodCell(
    center: np.ndarray | List[float] | Tuple,
    direction: np.ndarray | List[float] | Tuple,
    height: float,
    radius: float,
) -> RodCell:
    """
    Create a capsule (cylinder with spherical caps) shape.

    Args:
        center: Center point of the capsule
        direction: Direction vector of the capsule axis
        radius: Radius of both cylinder and spherical caps
        height: Height of the cylindrical portion (excluding caps)

    Returns:
        PVShape3D: Capsule shape instance
    """
    capsule = pv.Capsule(
        center=center, direction=direction, radius=radius, cylinder_length=height
    )

    return RodCell(
        mesh=capsule, center=center, direction=direction, height=height, radius=radius
    )


@dataclass
class RodCellParams:
    center: Vector3D
    direction: Vector3D
    height: float
    radius: float

    @classmethod
    def validate_center(cls, value):
        if not isinstance(value, (list, tuple, np.ndarray)) or len(value) != 3:
            raise ValueError("center must be a 3D vector")

    @classmethod
    def validate_direction(cls, value):
        if not isinstance(value, (list, tuple, np.ndarray)) or len(value) != 3:
            raise ValueError("direction must be a 3D vector")

    @classmethod
    def validate_height(cls, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("height must be a positive number")

    @classmethod
    def validate_radius(cls, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("radius must be a positive number")
