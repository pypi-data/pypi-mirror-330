from dataclasses import dataclass

import numpy as np
import pyvista as pv

from .base_cell import BASE_TOLERANCE, BaseCell


@dataclass
class RectangularCell(BaseCell):
    """
    Represents a rectangular cell in 3D space.

    Attributes:
        bounds (np.ndarray):
            [[xmin,xmax],[ymin,ymax],[zmin,zmax]]
    """

    bounds: np.ndarray

    def contains_point_fallback(
        self, x: float, y: float, z: float, tolerance: float = BASE_TOLERANCE
    ) -> bool:
        """
        Determines if a point (x, y, z) is inside the rectangular cell.

        Args:
            x (float): X-coordinate of the point
            y (float): Y-coordinate of the point
            z (float): Z-coordinate of the point

        Returns:
            bool: True if the point is inside the ovoid, False otherwise
        """
        # Convert single values to a point vector
        point = np.array([x, y, z])
        for i in range(len(point)):
            if (point[i] < self.bounds[i][0]) or (point[i] > self.bounds[i][1]):
                return False
        return True


def make_RectangularCell(bounds: np.ndarray) -> RectangularCell:
    """
    Parameters:
    -----------
    bounds (np.ndarray):
        [[xmin,xmax],[ymin,ymax],[zmin,zmax]]

    Returns:
    --------
    RectangularCell object
    """

    pv_bounds = np.asarray(bounds).flatten()
    rec = pv.Box(bounds=pv_bounds)
    return RectangularCell(mesh=rec, bounds=bounds)


@dataclass
class RectangularCellParams:
    bounds: np.ndarray

    @classmethod
    def validate_bounds(cls, value):
        if not isinstance(value, (list, tuple, np.ndarray)):
            raise ValueError("bounds must be an array-like object")

        # Convert to numpy array if needed
        if not isinstance(value, np.ndarray):
            value = np.array(value)

        # Check shape
        if value.shape != (3, 2):
            raise ValueError("bounds must be a 3x2 array (min and max points)")

        # Check min < max
        for i in range(3):
            if value[i, 0] >= value[i, 1]:
                raise ValueError(
                    f"Min bound must be less than max bound for dimension {i}"
                )
