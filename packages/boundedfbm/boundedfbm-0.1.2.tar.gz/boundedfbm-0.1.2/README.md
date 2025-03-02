# Multi-Dimensional Bounded FBM Simulator - with Time-Varying Diffusivity and Hurst Parameters

## Overview

This package provides tools for simulating bounded Fractional Brownian Motion (FBM) within 3D shapes created with PyVista. The simulator supports dynamic diffusion coefficients and Hurst exponents modeled as Markov chains, allowing for complex particle behavior simulation.

Key features:
- Creation of various 3D cell shapes (spherical, rod, rectangular, ovoid) using PyVista
- FBM simulation with time-varying diffusion coefficients
- Time-varying Hurst exponents for different motion regimes
- Markov chain modeling for parameter transitions
- Boundary handling for accurate confinement within cells

## Installation

```bash
pip install boundedfbm
```

## Quick Start

```python
import numpy as np
from boundedfbm import create_cell, CellType, FBM_BP

# 1. Create a cell to define boundaries
sphere_params = {
    "center": [0, 0, 0],
    "radius": 10.0
}
cell = create_cell(CellType.SPHERICAL, sphere_params)

# 2. Set up FBM parameters
n_steps = 1000  # Number of time steps
dt = 0.01       # Time step in seconds

# Single diffusion coefficient and Hurst exponent (simple case)
diffusion_params = np.array([1.0]) # length units of the pyvista models, time units of dt
hurst_params = np.array([0.7])  # Superdiffusive

# For state transitions, set up identity matrices (no transitions)
# probabilities are represented for a dt time event. 
diff_transition = np.array([[1.0]])
hurst_transition = np.array([[1.0]])

# Initial state probabilities (single state)
diff_prob = np.array([1.0])
hurst_prob = np.array([1.0])

# Initial position, represents the initial position of motion in the pyvista model
initial_position = np.array([0.0, 0.0, 0.0])

# 3. Create the FBM simulator
fbm_simulator = FBM_BP(
    n=n_steps,
    dt=dt,
    diffusion_parameters=diffusion_params,
    hurst_parameters=hurst_params,
    diffusion_parameter_transition_matrix=diff_transition,
    hurst_parameter_transition_matrix=hurst_transition,
    state_probability_diffusion=diff_prob,
    state_probability_hurst=hurst_prob,
    cell=cell,
    initial_position=initial_position
)

# 4. Run the simulation
trajectory = fbm_simulator.fbm(dims=3)

# 5. Visualize or analyze the results
# trajectory shape: (n_steps, 3) for 3D positions
```

## Creating Cells

The package supports several cell types that define boundaries for the FBM:

### Spherical Cell

```python
params = {
    "center": [0, 0, 0],   # 3D center coordinates
    "radius": 10.0         # Radius of sphere
}
cell = create_cell(CellType.SPHERICAL, params)
```

### Rod Cell

```python
params = {
    "center": [0, 0, 0],       # 3D center coordinates
    "direction": [0, 0, 1],    # Direction vector (will be normalized)
    "height": 20.0,            # Length of the rod
    "radius": 5.0              # Radius of the rod
}
cell = create_cell(CellType.ROD, params)
```

### Rectangular Cell

```python
params = {
    "bounds": [-10, 10, -10, 10, -10, 10]  # [xmin, xmax, ymin, ymax, zmin, zmax]
}
cell = create_cell(CellType.RECTANGULAR, params)
```

### Ovoid Cell

```python
params = {
    "center": [0, 0, 0],       # 3D center coordinates
    "direction": [0, 0, 1],    # Direction vector (will be normalized)
    "xradius": 10.0,           # Radius in x-direction
    "yradius": 15.0,           # Radius in y-direction
    "zradius": 20.0            # Radius in z-direction
}
cell = create_cell(CellType.OVOID, params)
```

## Advanced FBM Configuration

### Multi-State Diffusion and Hurst Parameters

You can model particles that switch between different motion regimes:

```python
# Two diffusion states: slow and fast
diffusion_params = np.array([0.5, 2.0])  

# Three Hurst states: subdiffusive, Brownian, and superdiffusive
hurst_params = np.array([0.3, 0.5, 0.7])  

# Transition matrices (probability of switching between states)
diff_transition = np.array([
    [0.95, 0.05],  # From state 0: 95% stay, 5% switch to state 1
    [0.10, 0.90]   # From state 1: 10% switch to state 0, 90% stay
])

hurst_transition = np.array([
    [0.90, 0.05, 0.05],  # From state 0
    [0.10, 0.80, 0.10],  # From state 1
    [0.05, 0.15, 0.80]   # From state 2
])

# Initial state probabilities
diff_prob = np.array([0.7, 0.3])  # 70% chance to start in state 0
hurst_prob = np.array([0.2, 0.5, 0.3])  # Initial distribution across 3 states
```

### Full Example with Multiple States and Visualization

```python
import numpy as np
import pyvista as pv
from boundedfbm import create_cell, CellType, FBM_BP

# Create a cell
cell_params = {
    "center": [0, 0, 0],
    "radius": 10.0
}
cell = create_cell(CellType.SPHERICAL, cell_params)

# Multi-state configuration
n_steps = 5000
dt = 0.01

# Two diffusion states
diffusion_params = np.array([0.5, 2.0])
diff_transition = np.array([
    [0.95, 0.05],
    [0.10, 0.90]
])
diff_prob = np.array([0.5, 0.5])

# Three Hurst exponent states
hurst_params = np.array([0.3, 0.5, 0.7])
hurst_transition = np.array([
    [0.90, 0.05, 0.05],
    [0.10, 0.80, 0.10],
    [0.05, 0.15, 0.80]
])
hurst_prob = np.array([0.33, 0.34, 0.33])

# Initial position
initial_position = np.array([0.0, 0.0, 0.0])

# Create simulator
fbm_simulator = FBM_BP(
    n=n_steps,
    dt=dt,
    diffusion_parameters=diffusion_params,
    hurst_parameters=hurst_params,
    diffusion_parameter_transition_matrix=diff_transition,
    hurst_parameter_transition_matrix=hurst_transition,
    state_probability_diffusion=diff_prob,
    state_probability_hurst=hurst_prob,
    cell=cell,
    initial_position=initial_position
)

# Run simulation
trajectory = fbm_simulator.fbm(dims=3)

# Visualize with PyVista
plotter = pv.Plotter()

# Add the cell geometry
cell_geometry = cell.get_shape()
plotter.add_mesh(cell_geometry, opacity=0.3, color='lightblue')

# Add the trajectory
points = np.array(trajectory) + initial_position  # Adjust by initial position
polyline = pv.PolyData(points)
polyline.lines = pv.lines_from_points(points)
plotter.add_mesh(polyline, line_width=2, color='red')

# Show the plot
plotter.show()
```

## Understanding FBM Parameters

### Diffusion Coefficient

The diffusion coefficient controls the magnitude of particle displacement. Higher values result in larger steps.

### Hurst Exponent

The Hurst exponent (H) controls the type of diffusion:
- H < 0.5: Subdiffusive motion (anti-persistent, tends to reverse direction)
- H = 0.5: Brownian motion (uncorrelated, classic random walk)
- H > 0.5: Superdiffusive motion (persistent, tends to continue in the same direction)

## API Reference

### Cell Creation

```python
from boundedfbm import create_cell, CellType

# Available cell types
CellType.SPHERICAL
CellType.ROD
CellType.RECTANGULAR
CellType.OVOID

# Create a cell
cell = create_cell(CellType.SPHERICAL, params)
```

### Parameter Validation

```python
from boundedfbm import validate_cell_parameters

# Check if parameters are valid
is_valid, errors = validate_cell_parameters(CellType.SPHERICAL, params)
```

### FBM Simulation

```python
from boundedfbm import FBM_BP

# Create simulator
simulator = FBM_BP(
    n=n_steps,                                   # Number of time steps
    dt=dt,                                       # Time step duration
    diffusion_parameters=diff_params,            # Array of diffusion coefficients
    hurst_parameters=hurst_params,               # Array of Hurst exponents
    diffusion_parameter_transition_matrix=dtm,   # Transition matrix for diffusion
    hurst_parameter_transition_matrix=htm,       # Transition matrix for Hurst
    state_probability_diffusion=diff_prob,       # Initial diffusion state probabilities
    state_probability_hurst=hurst_prob,          # Initial Hurst state probabilities
    cell=cell,                                   # Boundary cell
    initial_position=init_pos                    # Starting position
)

# Run the simulation
trajectory = simulator.fbm(dims=3)  # 3D simulation
```

## Advanced Topics

### Boundary Conditions

The simulator implements reflecting boundary conditions when a particle would cross the cell boundary.

### Optimizing Performance

For large simulations, consider:
- Pre-computing cell geometries when running multiple simulations

## License

MIT
