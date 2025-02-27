"""
# QRotor
 
The QRotor module is used to study the energy levels and wavefunctions of quantum rotations,
such as those of methyl and amine groups.
These quantum systems are represented by the `qrotor.System()` object.

QRotor can obtain custom potentials from DFT,
which are used to solve the quantum system.

This module uses meV as the default unit in the calculations.


# Index

| | |
| --- | --- |
| `aton.qrotor.system`    | Definition of the quantum `System` object |
| `aton.qrotor.systems`   | Functions to manage several System objects, such as a list of systems |
| `aton.qrotor.rotate`    | Rotate specific atoms from structural files |
| `aton.qrotor.constants` | Bond lengths and inertias |
| `aton.qrotor.potential` | Potential definitions and loading functions |
| `aton.qrotor.solve`     | Solve rotation eigenvalues and eigenvectors |
| `aton.qrotor.plot`      | Plotting functions |


# Examples

## Solving quantum rotational systems

A basic calculation of the eigenvalues for a zero potential goes as follows:

```python
import aton.qrotor as qr
system = qr.System()
system.gridsize = 200000  # Size of the potential grid
system.B = 1  # Rotational inertia
system.potential_name = 'zero'
system.solve()
system.eigenvalues
# [0.0, 1.0, 1.0, 4.0, 4.0, 9.0, 9.0, ...]  # approx values
```

The accuracy of the calculation increases with bigger gridsizes,
but note that the runtime increases exponentially.

The same calculation can be performed for a methyl group,
in a cosine potential of amplitude 30 meV:

```python
import aton.qrotor as qr
system = qr.System()
system.gridsize = 200000  # Size of the potential grid
system.B = qr.B_CH3  # Rotational inertia of a methyl group
system.potential_name = 'cosine'
system.potential_constants = [0, 30, 3, 0]  # Offset, max, freq, phase (for cos pot.)
system.solve()
# Plot potential and eigenvalues
qr.plot.energies(system)
# Plot the first wavefunctions
qr.plot.wavefunction(system, levels=[0,1,2], square=True)
```


## Custom potentials from DFT

QRotor can be used to obtain custom rotational potentials from DFT calculations.
Using Quantum ESPRESSO, running an SCF calculation for a methyl rotation every 10 degrees:

```python
import aton.qrotor as qr
from aton import interface
# Approx crystal positions of the atoms to rotate
atoms = [
    '1.101   1.204   1.307'
    '2.102   2.205   2.308'
    '3.103   3.206   3.309'
]
# Create the input SCF files, saving the filenames to a list
scf_files = qr.rotate.structure_qe('molecule.in', positions=atoms, angle=10, repeat=True)
# Run the Quantum ESPRESSO calculations
interface.slurm.sbatch(files=scf_files)
```

To load the calculated potential to a QRotor System,
```python
# Create a 'potential.dat' file with the potential as a function of the angle
qr.potential.from_qe()
# Load to the system
system = qr.potential.load()
# Solve the system, interpolating to a bigger gridsize
system.B = qr.B_CH3
system.solve(200000)
qr.plot.energies(system)
```


## Tunnel splittings and excitations

By default, energy eigenvalues are assumed to present triplet degeneracy,
see [A. J. Horsewill, Progress in Nuclear Magnetic Resonance Spectroscopy 35, 359–389 (1999)](https://doi.org/10.1016/S0079-6565(99)00016-3).
If this is not the case, check `aton.qrotor.solve.excitations()`.

When the quantum System is solved, tunnel splittings and excitations are also calculated:

```python
system.solve()
system.splittings
system.excitations
```

To export the tunnel splittings of several calculations to a CSV file:

```python
calculations = [system1, system2, system3]
qr.systems.splittings(calculations)
```


Check the API documentation for more details.

"""


from .system import System
from .constants import *
from . import systems
from . import rotate
from . import potential
from . import solve
from . import plot

