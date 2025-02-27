"""Module containing implementation of a class EMolecule for dealing with the chemical system and its geometry."""

import numpy as np
from mendeleev import element
from qiskit_nature.second_q.formats.molecule_info import MoleculeInfo
from qiskit_nature.units import DistanceUnit
import psi4


class EMolecule(MoleculeInfo):
    """
    Class containing information about the chemical system.
    """

    # TODO Is this class necessary or should be removed?

    def __init__(
        self,
        symbols,
        coords,
        multiplicity=1,
        charge=0,
        degrees_of_freedom=None,
        masses=None,
    ):
        self._geometry = [[symbol, coord] for symbol, coord in zip(symbols, coords)]
        super().__init__(
            self._geometry,
            multiplicity,
            charge,
            DistanceUnit.ANGSTROM,
            degrees_of_freedom,
            masses,
        )
        self._n_atoms = len(self._geometry)
        self._nuclear_repulsion_energy_gradient = None
        self._geometry_str = "\n".join(
            f"{atom[0]} " + " ".join(str(x) for x in atom[1]) for atom in self._geometry
        )

        # TODO is this necessary?
        self._geometry_str += "\nsymmetry c1\nnocom\nnoreorient\n"

        self._psi4_molecule = psi4.geometry(self._geometry_str, "PSI4 Molecule")

    @property
    def geometry(self):
        """Geometry in a list form."""
        return self._geometry

    @property
    def n_atoms(self):
        """Number of atoms"""
        return self._n_atoms

    @property
    def geometry_str(self):
        """Geometry in a text-string form"""
        return self._geometry_str

    @property
    def psi4_molecule(self):
        """Psi4 instance of Molecule class"""
        return self._psi4_molecule

    def _get_nuclear_repulsion_energy_gradient(self):
        de = []
        for i in range(self._n_atoms):
            entry = [0.0, 0.0, 0.0]
            for j in range(self._n_atoms):
                if i != j:
                    atom1 = self._geometry[i]
                    coord1 = atom1[1]
                    atom2 = self._geometry[j]
                    coord2 = atom2[1]

                    tmp = np.norm(coord1, coord2) ** 3.0

                    # Atomic numbers
                    zi = element(atom1[0]).atomic_number
                    zj = element(atom2[0]).atomic_number

                    # x-coordinates
                    entry[0] -= (coord1[0] - coord2[0]) * zi * zj / tmp

                    # y-coordinates
                    entry[1] -= (coord1[1] - coord2[1]) * zi * zj / tmp

                    # z-coordinates
                    entry[2] -= (coord1[2] - coord2[2]) * zi * zj / tmp

            de.append(entry)

        return de
