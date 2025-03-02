"""
Tests for Bounded FBM Simulator package.

This file contains pytest tests for verifying the functionality of:
1. Cell creation and validation
2. FBM simulation with different parameters
3. Boundary conditions
4. Markov chain state transitions
"""

import numpy as np
import pytest
import pyvista as pv
from numpy.testing import assert_array_equal

# Import package components
from boundedfbm import (
    FBM_BP,
    BaseCell,
    CellType,
    create_cell,
)
from boundedfbm.cells.cell_factory import validate_cell_parameters
from boundedfbm.probabilityfuncs.markov_chain import MCMC_state_selection

# ===== Cell Factory Tests =====


def test_cell_type_enum():
    """Test the CellType enum values."""
    assert CellType.SPHERICAL.value == "SphericalCell"
    assert CellType.ROD.value == "RodCell"
    assert CellType.RECTANGULAR.value == "RectangularCell"
    assert CellType.OVOID.value == "OvoidCell"

    # Test string conversion
    assert CellType("SphericalCell") == CellType.SPHERICAL
    assert CellType("RodCell") == CellType.ROD
    assert CellType("RectangularCell") == CellType.RECTANGULAR
    assert CellType("OvoidCell") == CellType.OVOID


def test_validate_spherical_cell_parameters():
    """Test validation of spherical cell parameters."""
    # Valid parameters
    params = {"center": [0, 0, 0], "radius": 10.0}
    is_valid, errors = validate_cell_parameters(CellType.SPHERICAL, params)
    assert is_valid
    assert not errors

    # Invalid: missing radius
    params = {"center": [0, 0, 0]}
    is_valid, errors = validate_cell_parameters(CellType.SPHERICAL, params)
    assert not is_valid
    assert any("radius" in error for error in errors)


def test_validate_rod_cell_parameters():
    """Test validation of rod cell parameters."""
    # Valid parameters
    params = {
        "center": [0, 0, 0],
        "direction": [0, 0, 1],
        "height": 20.0,
        "radius": 5.0,
    }
    is_valid, errors = validate_cell_parameters(CellType.ROD, params)
    assert is_valid
    assert not errors

    # Invalid: missing parameter
    params = {"center": [0, 0, 0], "direction": [0, 0, 1], "height": 20.0}
    is_valid, errors = validate_cell_parameters(CellType.ROD, params)
    assert not is_valid
    assert any("radius" in error for error in errors)


def test_validate_rectangular_cell_parameters():
    """Test validation of rectangular cell parameters."""
    # Valid parameters
    params = {"bounds": [-10, 10, -10, 10, -10, 10]}
    is_valid, errors = validate_cell_parameters(CellType.RECTANGULAR, params)
    assert is_valid
    assert not errors


def test_validate_ovoid_cell_parameters():
    """Test validation of ovoid cell parameters."""
    # Valid parameters
    params = {
        "center": [0, 0, 0],
        "direction": [0, 0, 1],
        "xradius": 10.0,
        "yradius": 15.0,
        "zradius": 20.0,
    }
    is_valid, errors = validate_cell_parameters(CellType.OVOID, params)
    assert is_valid
    assert not errors

    # Invalid: missing parameter
    params = {
        "center": [0, 0, 0],
        "direction": [0, 0, 1],
        "xradius": 10.0,
        "zradius": 20.0,
    }
    is_valid, errors = validate_cell_parameters(CellType.OVOID, params)
    assert not is_valid
    assert any("yradius" in error for error in errors)


def test_cell_factory_with_strings():
    """Test cell factory with string cell types."""
    params = {"center": [0, 0, 0], "radius": 10.0}

    # Valid string type
    cell = create_cell("SphericalCell", params)
    assert isinstance(cell, BaseCell)

    # Invalid string type
    with pytest.raises(ValueError):
        create_cell("NonExistentCell", params)


def test_create_spherical_cell():
    """Test creation of spherical cell."""
    params = {"center": [0, 0, 0], "radius": 10.0}
    cell = create_cell(CellType.SPHERICAL, params)
    assert isinstance(cell, BaseCell)

    # Test shape creation
    shape = cell.mesh
    assert isinstance(shape, pv.PolyData)

    # Test contains_point method
    assert cell.contains_point(0, 0, 0)  # Center should be inside
    assert cell.contains_point(5, 5, 5)  # Point inside
    assert not cell.contains_point(20, 0, 0)  # Point outside


def test_create_rod_cell():
    """Test creation of rod cell."""
    params = {
        "center": [0, 0, 0],
        "direction": [0, 0, 1],
        "height": 20.0,
        "radius": 5.0,
    }
    cell = create_cell(CellType.ROD, params)
    assert isinstance(cell, BaseCell)

    # Test contains_point method
    assert cell.contains_point(0, 0, 0)  # Center should be inside
    assert cell.contains_point(0, 0, 8)  # Point inside along axis
    assert cell.contains_point(3, 3, 5)  # Point inside
    assert not cell.contains_point(0, 0, 15)  # Point outside (too far along axis)
    assert not cell.contains_point(10, 0, 0)  # Point outside (too far from axis)


# ===== FBM Simulation Tests =====


def test_fbm_initialization():
    """Test initialization of FBM simulator."""
    # Create a simple spherical cell
    cell = create_cell(CellType.SPHERICAL, {"center": [0, 0, 0], "radius": 10.0})

    # Single state parameters
    n_steps = 100
    dt = 0.01
    diffusion_params = np.array([1.0])
    hurst_params = np.array([0.5])  # Brownian motion
    diff_transition = np.array([[1.0]])
    hurst_transition = np.array([[1.0]])
    diff_prob = np.array([1.0])
    hurst_prob = np.array([1.0])
    initial_position = np.array([0.0, 0.0, 0.0])

    # Create simulator
    simulator = FBM_BP(
        n=n_steps,
        dt=dt,
        diffusion_parameters=diffusion_params,
        hurst_parameters=hurst_params,
        diffusion_parameter_transition_matrix=diff_transition,
        hurst_parameter_transition_matrix=hurst_transition,
        state_probability_diffusion=diff_prob,
        state_probability_hurst=hurst_prob,
        cell=cell,
        initial_position=initial_position,
    )

    # Check if simulator was created correctly
    assert simulator.n == n_steps
    assert simulator.dt == dt
    assert simulator.randomwalkers  # H=0.5 should set randomwalkers=True
    assert_array_equal(simulator.diffusion_parameter, diffusion_params)
    assert_array_equal(simulator.hurst_parameter, hurst_params)


def test_fbm_simulation_output():
    """Test the output shape and properties of FBM simulation."""
    # Create a simple spherical cell
    cell = create_cell(
        CellType.SPHERICAL, {"center": [0, 0, 0], "radius": 100.0}
    )  # Large radius to avoid boundary issues in this test

    # Simple FBM parameters
    n_steps = 50
    dt = 0.01
    diffusion_params = np.array([1.0])
    hurst_params = np.array([0.5])  # Brownian motion
    diff_transition = np.array([[1.0]])
    hurst_transition = np.array([[1.0]])
    diff_prob = np.array([1.0])
    hurst_prob = np.array([1.0])
    initial_position = np.array([0.0, 0.0, 0.0])

    # Create simulator
    simulator = FBM_BP(
        n=n_steps,
        dt=dt,
        diffusion_parameters=diffusion_params,
        hurst_parameters=hurst_params,
        diffusion_parameter_transition_matrix=diff_transition,
        hurst_parameter_transition_matrix=hurst_transition,
        state_probability_diffusion=diff_prob,
        state_probability_hurst=hurst_prob,
        cell=cell,
        initial_position=initial_position,
    )

    # Run simulation
    trajectory = simulator.fbm(dims=3)

    # Check output shape
    assert trajectory.shape == (n_steps, 3)

    # First position should be zero
    assert_array_equal(trajectory[0], np.zeros(3))

    # Trajectory should have non-zero displacement
    assert not np.all(trajectory[-1] == np.zeros(3))


def test_boundary_conditions():
    """Test that particles remain within boundaries."""
    # Create a small spherical cell to force boundary interactions
    radius = 5.0
    cell = create_cell(CellType.SPHERICAL, {"center": [0, 0, 0], "radius": radius})

    # FBM parameters with large diffusion to ensure boundary interactions
    n_steps = 200
    dt = 0.01
    diffusion_params = np.array([10.0])  # Large diffusion coefficient
    hurst_params = np.array([0.7])  # Superdiffusive for persistent motion
    diff_transition = np.array([[1.0]])
    hurst_transition = np.array([[1.0]])
    diff_prob = np.array([1.0])
    hurst_prob = np.array([1.0])
    initial_position = np.array([0.0, 0.0, 0.0])

    # Create simulator
    simulator = FBM_BP(
        n=n_steps,
        dt=dt,
        diffusion_parameters=diffusion_params,
        hurst_parameters=hurst_params,
        diffusion_parameter_transition_matrix=diff_transition,
        hurst_parameter_transition_matrix=hurst_transition,
        state_probability_diffusion=diff_prob,
        state_probability_hurst=hurst_prob,
        cell=cell,
        initial_position=initial_position,
    )

    # Run simulation
    trajectory = simulator.fbm(dims=3)

    # Check that all points are within the cell radius
    # (adding initial_position since the trajectory is relative to it)
    absolute_positions = trajectory + initial_position
    distances = np.linalg.norm(absolute_positions, axis=1)

    # Allow small numerical tolerance
    assert np.all(
        distances <= radius * 1.001
    ), f"Some positions exceed the cell radius: max={np.max(distances)}, radius={radius}"


def test_markov_chain_transitions():
    """Test Markov chain state selection for parameter transitions."""
    # Set up a simple two-state Markov chain
    transition_matrix = np.array([[0.8, 0.2], [0.3, 0.7]])
    states = np.array([1.0, 2.0])
    n_steps = 1000

    # Run the chain starting from state 0
    state_sequence = MCMC_state_selection(0, transition_matrix, states, n_steps)

    # Check the shape of the output
    assert len(state_sequence) == n_steps

    # Check that only valid states are present
    assert np.all(np.isin(state_sequence, states))

    # Calculate empirical transition probabilities
    if len(state_sequence) > 100:  # Only check if we have enough samples
        state_0_indices = np.where(state_sequence[:-1] == states[0])[0]
        if len(state_0_indices) > 0:
            transitions_from_0_to_1 = np.sum(
                state_sequence[state_0_indices + 1] == states[1]
            )
            empirical_prob_0_to_1 = transitions_from_0_to_1 / len(state_0_indices)

            # Allow for some statistical variation
            assert abs(empirical_prob_0_to_1 - transition_matrix[0, 1]) < 0.1


def test_multi_state_fbm():
    """Test FBM with multiple diffusion and Hurst states."""
    # Create a spherical cell
    cell = create_cell(CellType.SPHERICAL, {"center": [0, 0, 0], "radius": 20.0})

    # Two diffusion states and two Hurst states
    n_steps = 100
    dt = 0.01
    diffusion_params = np.array([0.5, 2.0])
    hurst_params = np.array([0.3, 0.7])

    # Transition matrices with high probability of staying in same state
    diff_transition = np.array([[0.9, 0.1], [0.1, 0.9]])
    hurst_transition = np.array([[0.9, 0.1], [0.1, 0.9]])

    # Initial state probabilities
    diff_prob = np.array([0.5, 0.5])
    hurst_prob = np.array([0.5, 0.5])

    initial_position = np.array([0.0, 0.0, 0.0])

    # Create simulator
    simulator = FBM_BP(
        n=n_steps,
        dt=dt,
        diffusion_parameters=diffusion_params,
        hurst_parameters=hurst_params,
        diffusion_parameter_transition_matrix=diff_transition,
        hurst_parameter_transition_matrix=hurst_transition,
        state_probability_diffusion=diff_prob,
        state_probability_hurst=hurst_prob,
        cell=cell,
        initial_position=initial_position,
    )

    # Checking if the internal state arrays were properly set up
    assert len(simulator._diff_a_n) == n_steps
    assert len(simulator._hurst_n) == n_steps

    # Verify that values are only from the parameter arrays
    assert np.all(np.isin(simulator._diff_a_n, diffusion_params))
    assert np.all(np.isin(simulator._hurst_n, hurst_params))

    # Run simulation
    trajectory = simulator.fbm(dims=3)

    # Check output shape
    assert trajectory.shape == (n_steps, 3)


def test_different_hurst_values():
    """Test FBM with different Hurst exponents and verify expected behavior."""
    # Create a large spherical cell to minimize boundary effects
    cell = create_cell(CellType.SPHERICAL, {"center": [0, 0, 0], "radius": 100.0})

    n_steps = 500
    dt = 0.01
    diffusion_param = 1.0
    initial_position = np.array([0.0, 0.0, 0.0])

    # Test different Hurst exponents
    hurst_values = [0.3, 0.5, 0.7]  # subdiffusive, Brownian, superdiffusive

    msd_results = []  # Mean squared displacement

    for hurst in hurst_values:
        # Create simulator with single Hurst value
        simulator = FBM_BP(
            n=n_steps,
            dt=dt,
            diffusion_parameters=np.array([diffusion_param]),
            hurst_parameters=np.array([hurst]),
            diffusion_parameter_transition_matrix=np.array([[1.0]]),
            hurst_parameter_transition_matrix=np.array([[1.0]]),
            state_probability_diffusion=np.array([1.0]),
            state_probability_hurst=np.array([1.0]),
            cell=cell,
            initial_position=initial_position,
        )

        # Run multiple simulations to get average behavior
        n_simulations = 10
        final_distances = []

        for _ in range(n_simulations):
            trajectory = simulator.fbm(dims=3)
            # Calculate final distance from origin
            final_distance = np.linalg.norm(trajectory[-1])
            final_distances.append(final_distance)

        # Calculate mean squared displacement
        msd = np.mean(np.square(final_distances))
        msd_results.append(msd)

    # For FBM, MSD scales as t^(2H), so higher Hurst should give larger MSD
    # Check if MSD increases with Hurst exponent
    assert (
        msd_results[0] < msd_results[1] < msd_results[2]
    ), f"MSDs not increasing with Hurst: {msd_results}"
