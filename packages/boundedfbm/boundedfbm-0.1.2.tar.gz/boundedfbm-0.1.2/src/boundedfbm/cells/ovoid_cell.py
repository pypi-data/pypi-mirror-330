from dataclasses import dataclass

import numpy as np
import pyvista as pv

from .base_cell import BASE_TOLERANCE, BaseCell
from .typedefs import Vector3D


@dataclass
class OvoidCell(BaseCell):
    """
    Represents an ovoid (ellipsoidal) cell in 3D space, centered around Z=0.
    Attributes:
        center (np.ndarray): The (x, y, z) coordinates of the cell's center in XYZ
        direction (np.ndarray): direction vector of the orientation of the ovoid
        xradius (float): Radius along the X axis
        yradius (float): Radius along the Y axis
        zradius (float): Radius along the Z axis
    """

    center: np.ndarray
    direction: np.ndarray
    xradius: float
    yradius: float
    zradius: float

    def __post_init__(self):
        super().__post_init__() if hasattr(super(), "__post_init__") else None
        # Precalculate rotation matrix and other constants for point containment checks
        self._setup_containment_check()

    def _setup_containment_check(self):
        """
        Precalculates values needed for the is_point_inside method to improve performance.
        """
        # Normalize the direction vector
        direction_normalized = self.direction / np.linalg.norm(self.direction)

        # Standard z-axis
        z_axis = np.array([0, 0, 1])

        # Find the rotation axis (cross product) and angle (dot product)
        rotation_axis = np.cross(direction_normalized, z_axis)

        # Handle the case when vectors are already aligned or opposite
        if np.allclose(rotation_axis, 0):
            if np.dot(direction_normalized, z_axis) > 0:
                # Vectors are already aligned, no rotation needed
                self._rotation_matrix = np.eye(3)
            else:
                # Vectors are opposite, rotate 180 degrees around x-axis
                self._rotation_matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
        else:
            # Normal case: calculate rotation matrix using the Rodrigues formula
            rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
            cos_angle = np.dot(direction_normalized, z_axis)
            sin_angle = np.linalg.norm(np.cross(direction_normalized, z_axis))

            # Skew-symmetric matrix for cross product
            K = np.array(
                [
                    [0, -rotation_axis[2], rotation_axis[1]],
                    [rotation_axis[2], 0, -rotation_axis[0]],
                    [-rotation_axis[1], rotation_axis[0], 0],
                ]
            )

            # Rodrigues formula
            self._rotation_matrix = (
                np.eye(3) + sin_angle * K + (1 - cos_angle) * (K @ K)
            )

        # Precalculate squared reciprocals of radii for faster calculation
        self._x_radius_sq_recip = 1.0 / (self.xradius**2)
        self._y_radius_sq_recip = 1.0 / (self.yradius**2)
        self._z_radius_sq_recip = 1.0 / (self.zradius**2)

    def contains_point_fallback(
        self, x: float, y: float, z: float, tolerance: float = BASE_TOLERANCE
    ) -> bool:
        """
        Determines if a point (x, y, z) is inside the ovoid cell.
        Uses precalculated values for efficiency.

        Args:
            x (float): X-coordinate of the point
            y (float): Y-coordinate of the point
            z (float): Z-coordinate of the point

        Returns:
            bool: True if the point is inside the ovoid, False otherwise
        """
        # Convert single values to a point vector
        point = np.array([x, y, z])

        # Translate point to ovoid's coordinate system (origin at center)
        translated_point = point - self.center

        # Apply rotation to align with standard axes
        rotated_point = self._rotation_matrix @ translated_point

        # Check if the point is inside the ellipsoid using the standard equation
        # (x/a)² + (y/b)² + (z/c)² <= 1
        # Using precalculated squared reciprocals for efficiency
        inside = (
            (rotated_point[0] ** 2) * self._x_radius_sq_recip
            + (rotated_point[1] ** 2) * self._y_radius_sq_recip
            + (rotated_point[2] ** 2) * self._z_radius_sq_recip
        ) <= 1.0

        return inside


def make_OvoidCell(
    center: np.ndarray,
    direction: np.ndarray,
    xradius: float,
    yradius: float,
    zradius: float,
) -> OvoidCell:
    return OvoidCell(
        mesh=pv.ParametricEllipsoid(
            xradius=xradius,
            yradius=yradius,
            zradius=zradius,
            center=center,
            direction=direction,
        ),
        center=center,
        direction=direction,
        xradius=xradius,
        yradius=yradius,
        zradius=zradius,
    )


@dataclass
class OvoidCellParams:
    center: Vector3D
    direction: Vector3D
    xradius: float
    yradius: float
    zradius: float

    @classmethod
    def validate_center(cls, value):
        if not isinstance(value, (list, tuple, np.ndarray)) or len(value) != 3:
            raise ValueError("center must be a 3D vector")

    @classmethod
    def validate_direction(cls, value):
        if not isinstance(value, (list, tuple, np.ndarray)) or len(value) != 3:
            raise ValueError("direction must be a 3D vector")

    @classmethod
    def validate_xradius(cls, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("xradius must be a positive number")

    @classmethod
    def validate_yradius(cls, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("yradius must be a positive number")

    @classmethod
    def validate_zradius(cls, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("zradius must be a positive number")
