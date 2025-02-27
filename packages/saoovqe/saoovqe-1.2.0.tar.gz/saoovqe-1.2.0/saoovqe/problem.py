"""Module enabling definition of the problem to solve.

Module containing ProblemSet class, which comprises all the information
about the relevant electronic structure problem together with all
the operators and performs all the necessary operations like active
space transformations etc.
"""

from typing import Union, Optional

from qiskit_nature.second_q.drivers import Psi4Driver
from qiskit_nature.second_q.formats import get_ao_to_mo_from_qcschema
from qiskit_nature.second_q.hamiltonians import ElectronicEnergy
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.mappers.fermionic_mapper import FermionicMapper
from qiskit_nature.second_q.operators import (
    FermionicOp,
    SparseLabelOp,
    ElectronicIntegrals,
)
from qiskit_nature.second_q.problems import ElectronicStructureProblem, ElectronicBasis
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer, BasisTransformer
from qiskit.quantum_info import SparsePauliOp

import numpy as np
import psi4

from .logger_config import log
from .molecule import EMolecule


class ProblemSet:
    """
    Class containing relevant instances of ElectronicStructureProblem
    together with their operators and transformers.
    It comprises all the information about the problem being solver
    including the aggregated chemistry driver.
    """

    @classmethod
    def with_dia_orbs_from_prev_wfn(
        cls,
        symbols: list[str],
        coords: list[list],
        charge: int,
        multiplicity: int,
        n_electrons_active: int,
        n_orbitals_active: int,
        prev_wfn: psi4.core.RHF,
        basis_name: str = "sto-3g",
        fermionic_mapper: FermionicMapper = JordanWignerMapper(),
    ):
        """
        Constructor for ProblemSet allowing passing of a wavefunction belonging to previous point (geometry)
        for computations in a chain-like manner. Subsequently, it performs diabatization of the orbitals, before
        they're used.

        :param symbols: Symbols of atoms in molecule
        :param coords: Coordinates of atoms
        :param charge: System's charge
        :param multiplicity: System's multiplicity
        :param n_electrons_active: Number of electrons present in an active space
        :param n_orbitals_active: Number of molecular orbitals present in an active space
        :param prev_wfn: Wavefunction for the previous geometry in the computation
        :param basis_name: Name of the basis set used in preliminary SCF computation
        :param fermionic_mapper: Instance of FermionicMapper to map necessary operators to qubits
        :return: An instance of ProblemSet
        """

        # TODO finish the initializer
        # TODO add the private method for diabatization of orbitals

        instance = cls(
            symbols,
            coords,
            charge,
            multiplicity,
            n_electrons_active,
            n_orbitals_active,
            basis_name=basis_name,
            fermionic_mapper=fermionic_mapper,
        )

        # Orbital diabatization
        orbitals = instance._psi4_wfn.Ca().np.copy()

        s_ao = np.asarray(
            instance._psi4_mints.ao_overlap(
                prev_wfn.basisset(), instance._psi4_wfn.basisset()
            )
        )
        s_casscf = (
            prev_wfn.Ca().np[:, instance.active_orbitals].T
            @ s_ao
            @ orbitals[:, instance.active_orbitals]
        )

        # Compute diabatic orbitals, the ordering might change, which is what we want:
        # we want the same orbital ordering that the final point (after SAOO), to start with the correct Phi_B.
        # active space:
        sdag_s = s_casscf @ s_casscf.T
        eigval, eigvec = np.linalg.eigh(sdag_s)
        sdag_s_invsqrt = eigvec @ np.diag(eigval ** (-1.0 / 2.0)) @ eigvec.T
        transformation = s_casscf.T @ sdag_s_invsqrt
        orbitals[:, instance.active_orbitals] = (
            orbitals[:, instance.active_orbitals] @ transformation
        )

        instance._psi4_wfn.Ca().np[:] = orbitals
        instance._c_mat = orbitals

        # TODO rewrite so that the following code is not duplicated
        # PSI4 object for working with 1- and 2-body integrals
        # TODO remove, when possible!
        instance._psi4_mints = psi4.core.MintsHelper(instance._psi4_wfn.basisset())
        instance._full_ham_one_body_integrals_ao = np.array(
            instance._psi4_mints.ao_kinetic()
        ) + np.array(instance._psi4_mints.ao_potential())
        instance._n_atomic_orbitals = np.shape(
            instance._full_ham_one_body_integrals_ao
        )[0]
        instance._full_ham_two_body_integrals_ao = np.array(
            instance._psi4_mints.ao_eri()
        ).reshape((instance._n_atomic_orbitals,) * 4)
        instance._full_ham_ao_integrals = ElectronicIntegrals.from_raw_integrals(
            instance._full_ham_one_body_integrals_ao,
            instance._full_ham_two_body_integrals_ao,
        )

        instance.update_problem_from_mo_coeffs(orbitals)
        return instance

    def __init__(
        self,
        symbols: list[str],
        coords: list[list],
        charge: int,
        multiplicity: int,
        n_electrons_active: int,
        n_orbitals_active: int,
        basis_name: str = "sto-3g",
        fermionic_mapper: FermionicMapper = JordanWignerMapper(),
        wfn: Optional[tuple[np.ndarray, bool]] = None,
        psi4_out_file: str = 'psi4-rhf.out',
    ):
        """
        Constructor for ProblemSet allowing passing of a wavefunction belonging to previous point (geometry)
        for computations in a chain-like manner. Subsequently, if the previous geometry wavefunction was provided,
        it performs diabatization of the orbitals, before they're used.

        :param symbols: Symbols of atoms in molecule
        :param coords: Coordinates of atoms
        :param charge: System's charge
        :param multiplicity: System's multiplicity
        :param n_electrons_active: Number of electrons present in an active space
        :param n_orbitals_active: Number of molecular orbitals present in an active space
        :param wfn: Wavefunction provided by the user
        :param basis_name: Name of the basis set used in preliminary SCF computation
        :param fermionic_mapper: Instance of FermionicMapper to map necessary operators to qubits
        :param psi4_out_file: The name of the Psi4 output file. Useful especially when running multiple instances of
        the solver.
        """

        # Define unit constants
        self._unit_constants = {"Bohr_to_Angstrom": 0.5291772105638411}

        # Create EMolecule using the provided symbols and coordinates
        self._molecule = EMolecule(
            symbols=symbols, coords=coords, charge=charge, multiplicity=multiplicity
        )

        # Set other attributes
        self._basis_name = basis_name
        self._n_orbitals_active = n_orbitals_active

        # Active space transformer
        self._active_space_transformer = ActiveSpaceTransformer(
            num_electrons=n_electrons_active,
            num_spatial_orbitals=self._n_orbitals_active,
        )

        # Construct PSI4 input
        labels = "".join(symbols)
        coords = "\n".join(
            f'{symbol} {" ".join(map(str, coord))}'
            for symbol, coord in zip(symbols, coords)
        )
        psi4_input = (
            f"molecule {labels} {{\n"
            f"units ang\n"
            f"{coords}\n"
            f"symmetry c1\n"
            f"no_com\n"
            f"no_reorient\n}}\n\n"
            f"set {{\n basis {self._basis_name}\n scf_type pk\n"
            f"reference rhf\n}}"
        )

        # PSI4 Moleculer driver running initial SCF calculations and
        # assembling operators
        self._molecule_driver = Psi4Driver(psi4_input)

        # Full ElectronicStructureProblem instance, without further
        # transformation
        self._full_problem = self._molecule_driver.run()
        self._full_problem_qcschema = self._molecule_driver.to_qcschema()

        # BasisTransformer instance - for performing AO->MO transformation
        # and obtaining MO coefficients
        self._basis_transformer = get_ao_to_mo_from_qcschema(
            self._full_problem_qcschema
        )

        # Electronic-structure problem after active-space transformation
        self._as_problem = self._active_space_transformer.transform(self._full_problem)

        # self._full_ops = list(self._full_problem.second_q_ops())
        self._as_ops = list(self._as_problem.second_q_ops())

        # Total number of molecular orbitals without active-space
        # transformation
        self._n_molecular_orbitals = self.full_problem.num_spatial_orbitals
        # Determine indices of active orbitals in the full orbital space
        # based on total number of electrons and orbitals
        self._active_orbitals = self._active_space_transformer._determine_active_space(
            self.full_problem.num_particles[0] + self.full_problem.num_particles[1],
            self._n_molecular_orbitals,
        )
        # Only take alpha spin orbitals
        self._active_orbitals = self._active_orbitals[0]

        self._frozen_orbitals_indices = list(range(self._active_orbitals[0]))

        self._virtual_orbitals_indices = list(
            range(self._active_orbitals[-1] + 1, self._n_molecular_orbitals)
        )

        # One-body electronic integrals from FULL Hamiltonian
        #
        # Paper notation: h
        self._full_ham_one_body_integrals_mo = (
            self._full_problem.hamiltonian.electronic_integrals.one_body.alpha["+-"]
        )

        # Two-body electronic integrals from FULL Hamiltonian
        #
        # Paper notation: g
        self._full_ham_two_body_integrals_mo = np.einsum(
            "ijkl->ljik",
            self._full_problem.hamiltonian.electronic_integrals.two_body.alpha["++--"],
        )

        # Necessary shifts to obtain the total energy from ACTIVE Hamiltonian
        self._nuclear_repulsion_eng = self._as_problem.nuclear_repulsion_energy
        self._transform_eng_shift = self._as_problem.hamiltonian.constants[
            "ActiveSpaceTransformer"
        ]

        # Active-space Hamiltonian
        self._second_q_active_ham_op = self._as_ops[0]

        # TODO only for debug
        # TODO remove constant terms from Hamiltonian itself later - only
        #  add it to results to mitigate noise!
        tmp = self._second_q_active_ham_op._data.copy()
        tmp[""] = self.nuclear_repulsion_eng + self.transform_eng_shift
        test = FermionicOp(tmp, num_spin_orbitals=self._as_problem.num_spin_orbitals)
        self._second_q_active_ham_op = test

        # All one-body excitation operator terms
        # Initialized on-demand when computing gradients
        #
        # Paper notation: \widehat{E}_{pq}
        self._one_body_exc_op_active: Union[list[list[FermionicOp]], None] = None
        self._one_body_exc_op_full: Union[list[list[FermionicOp]], None] = None

        # All two-body excitation operator terms
        # Initialized on-demand when computing graidents
        #
        # Paper notation: \widehat{e}_{pqrs}
        self._two_body_exc_op_active: Union[
            list[list[list[list[FermionicOp]]]], None
        ] = None
        self._two_body_exc_op_full: Union[
            list[list[list[list[FermionicOp]]]], None
        ] = None

        # Transformation to Pauli strings
        self._fermionic_mapper = fermionic_mapper

        # Active Hamiltonian - for SA-VQE
        self._qubit_active_hamiltonian = self._fermionic_mapper.map(
            self._second_q_active_ham_op
        )

        self._second_q_active_s_squared_op = self._as_ops[1]["AngularMomentum"]
        self._qubit_active_s_squared_op = self._fermionic_mapper.map(
            self._second_q_active_s_squared_op
        )

        # Nuclear derivative of Hamiltonian
        #   Paper notation: \frac{d\widehat{H}}{dx}
        #
        # Initialized on demand in lazy-loading manner
        self._second_q_ham_nuc_deriv_op: list[list[None | FermionicOp]] = [
            [None for _ in range(3)] for __ in range(self.molecule.n_atoms)
        ]
        self._qubit_ham_nuc_deriv_op = [
            [None for _ in range(3)] for __ in range(self.molecule.n_atoms)
        ]

        # Nuclear derivatives of 1- and 2-body integrals in electronic
        # Hamiltonian
        #
        #   Paper notation: \frac{\partial h_{pq}}{\partial x},
        #   \frac{\partial g_{pqrs}}{\partial x}
        self._one_body_el_int_nuc_der: list[None | np.ndarray] = [
            None
        ] * self.molecule.n_atoms
        self._two_body_el_int_nuc_der: list[None | np.ndarray] = [
            None
        ] * self.molecule.n_atoms
        self._one_body_el_int_nuc_der_transformed: list[None | np.ndarray] = [
            None
        ] * self.molecule.n_atoms
        self._two_body_el_int_nuc_der_transformed: list[None | np.ndarray] = [
            None
        ] * self.molecule.n_atoms

        # Explicit derivative terms
        #
        # Paper notation: h^{(x)}_{pq}, g^{(x)}_{pqrs}, S^{(x)}_{pq}
        self._enuc_deriv = [None] * self.molecule.n_atoms
        self._ao_one_body_el_int_nuc_der_explicit = [None] * self.molecule.n_atoms
        self._ao_two_body_el_int_nuc_der_explicit = [None] * self.molecule.n_atoms
        self._ao_overlap_el_int_nuc_der_explicit = [None] * self.molecule.n_atoms
        self._mo_one_body_el_int_nuc_der_explicit = [None] * self.molecule.n_atoms
        self._mo_two_body_el_int_nuc_der_explicit = [None] * self.molecule.n_atoms
        self._mo_overlap_el_int_nuc_der_explicit = [None] * self.molecule.n_atoms

        # Molecular orbital coefficients (allows for transformation between
        # atomic and molecular orbital basis)
        # TODO is taking only alpha coefficients ok?
        self._c_mat = self._basis_transformer.coefficients.alpha["+-"]

        # Compute wavefunction via Psi4, if one wasn't provided directly
        if wfn is None:
            # TODO remove direct call to Psi4, when the plugin for Qiskit is done!
            psi4.core.clean()
            psi4.core.clean_variables()
            psi4.core.clean_options()
            psi4.set_options(
                {"basis": self.basis_name, "reference": "rhf", "SCF_TYPE": "pk"}
            )
            psi4.core.set_output_file("psi4-rhf.out", append=False)
            _, self._psi4_wfn = psi4.energy(
                "HF", molecule=self.molecule.psi4_molecule, return_wfn=True, verbose=0
            )

        else:
            self._psi4_wfn = wfn

        # PSI4 object for working with 1- and 2-body integrals
        # TODO remove, when possible!
        self._psi4_mints = psi4.core.MintsHelper(self._psi4_wfn.basisset())

        self._full_ham_one_body_integrals_ao = np.array(
            self._psi4_mints.ao_kinetic()
        ) + np.array(self._psi4_mints.ao_potential())
        self._n_atomic_orbitals = (np.shape(self._full_ham_one_body_integrals_ao))[0]
        self._full_ham_two_body_integrals_ao = np.array(
            self._psi4_mints.ao_eri()
        ).reshape((self._n_atomic_orbitals,) * 4)
        self._full_ham_ao_integrals = ElectronicIntegrals.from_raw_integrals(
            self._full_ham_one_body_integrals_ao, self._full_ham_two_body_integrals_ao
        )

        log.info("SecondQuantizedProblem was created.")

    @property
    def psi4_mints(self):
        """
        Psi4 molecular integrals.
        """
        return self._psi4_mints

    @property
    def unit_constants(self) -> dict[str, float]:
        """
        Constants used for unit conversions.
        """
        return self._unit_constants

    @property
    def geometry_str(self) -> Optional[str]:
        """
        Geometry string used in Psi4 calculations.
        """
        return self._molecule.geometry_str

    @property
    def c_mat(self) -> np.ndarray:
        """
        Matrix of molecular orbitals coefficients.
        """
        return self._c_mat

    @property
    def full_problem(self) -> ElectronicStructureProblem:
        """
        The full electronic structure problem instance, before any
        transformation applied.
        """
        return self._full_problem

    @property
    def as_problem(self) -> ElectronicStructureProblem:
        """
        The instance of electronic structure problem after active space
        transformation.
        """
        return self._as_problem

    @property
    def n_qubits(self):
        """
        Number of qubits used to encode an active-space Hamiltonian.
        """
        return self._second_q_active_ham_op.register_length

    @property
    def e_nuc_der(self):
        """
        Derivative of nuclear energy repulsion as computed by Psi4.
        """
        return self._enuc_deriv

    @property
    def one_body_el_int_nuc_der_explicit_ao(self):
        """
        Nuclear derivatives of 1-body electronic integrals in atomic-orbital
        basis.
        """
        return self._ao_one_body_el_int_nuc_der_explicit

    @property
    def two_body_el_int_nuc_der_explicit_ao(self):
        """
        Nuclear derivatives of 2-body electronic integrals in atomic-orbital
        basis.
        """
        return self._ao_two_body_el_int_nuc_der_explicit

    @property
    def overlap_el_int_nuc_der_explicit_ao(self):
        """
        Nuclear derivatives of overlap electronic integrals in
        atomic-orbital basis.
        """
        return self._ao_overlap_el_int_nuc_der_explicit

    @property
    def one_body_el_int_nuc_der_explicit_mo(self):
        """
        Nuclear derivatives of 1-body electronic integrals in
        molecular-orbital basis.
        """
        return self._mo_one_body_el_int_nuc_der_explicit

    @property
    def two_body_el_int_nuc_der_explicit_mo(self):
        """
        Nuclear derivatives of 2-body electronic integrals in
        molecular-orbital basis.
        """
        return self._mo_two_body_el_int_nuc_der_explicit

    @property
    def overlap_el_int_nuc_der_explicit_mo(self):
        """
        Nuclear derivatives of overlap electronic integrals in
        molecular-orbital basis.
        """
        return self._mo_overlap_el_int_nuc_der_explicit

    @property
    def molecule(self) -> EMolecule:
        """
        Instance comprising the information about the molecule itself like
        its geometry, elements etc.
        """
        return self._molecule

    @property
    def basis_name(self) -> str:
        """
        Name of the basis set used for the initial HF computation.
        """
        return self._basis_name

    @property
    def n_molecular_orbitals(self) -> int:
        """
        Number of molecular orbitals in the full electronic structure
        problem, i.e. before any transformation happened.
        """
        return self._n_molecular_orbitals

    @property
    def n_orbitals_active(self) -> int:
        """
        Number of molecular orbitals in the active-space-transformed
        electronic structure problem.
        """
        return self._n_orbitals_active

    @property
    def n_orbitals_frozen(self) -> int:
        """
        Number of frozen orbitals (in the active-space-transformed
        electronic structure problem).
        """
        return len(self._frozen_orbitals_indices)

    @property
    def n_orbitals_virtual(self) -> int:
        """
        Number of virtual orbitals (in the active-space-transformed
        electronic structure problem).
        """
        return len(self._virtual_orbitals_indices)

    @property
    def active_orbitals(self) -> list[int]:
        """
        Indices of the active orbitals (in the active-space-transformed
        electronic structure problem).
        """
        return self._active_orbitals

    @property
    def frozen_orbitals_indices(self) -> list[int]:
        """
        Indices of the frozen orbitals (in the active-space-transformed
        electronic structure problem).
        """
        return self._frozen_orbitals_indices

    @property
    def virtual_orbitals_indices(self) -> list[int]:
        """
        Indices of the virtual orbitals (in the active-space-transformed
        electronic structure problem).
        """
        return self._virtual_orbitals_indices

    @property
    def active_space_transformer(self) -> ActiveSpaceTransformer:
        """
        Instance of the used active space transformer.
        """
        return self._active_space_transformer

    @property
    def molecule_driver(self) -> Psi4Driver:
        """
        Instance of Psi4 driver performing initial HF computation and
        providing some derivatives in atomic-orbital
        basis.
        """
        return self._molecule_driver

    @property
    def as_operators(self) -> list[SparseLabelOp, dict[str, SparseLabelOp]]:
        """
        Operators in active space transformed electronic structure problem.
        """
        return self._as_ops

    # @property
    # def full_operators(self) -> list[SparseLabelOp, dict[str,
    # SparseLabelOp]]:
    #     """
    #     Operators in the full electronic structure problem (without any
    #     transformation).
    #     """
    #     return self._full_ops

    @property
    def fermionic_mapper(self):
        """
        Instance of mapper used to map fermionic operators to qubits.
        """
        return self._fermionic_mapper

    @property
    def qubit_active_hamiltonian(self):
        """
        Hamiltonian in the active-space-transformed electronic structure
        problem.
        """
        return self._qubit_active_hamiltonian

    @property
    def one_body_exc_op_active(self):
        """
        1-body excitation operator (part of Hamiltonian) in the
        active-space-transformed electronic structure problem.
        """
        return self._one_body_exc_op_active

    @property
    def two_body_exc_op_active(self):
        """
        2-body excitation operator (part of Hamiltonian) in the
        active-space-transformed electronic structure problem.
        """
        return self._two_body_exc_op_active

    @property
    def qubit_s_squared(self):
        """
        S^2 operator in the active-space-transformed electronic structure
        problem.
        """
        return self._qubit_active_s_squared_op

    @property
    def nuclear_repulsion_eng(self):
        """
        Nuclear repulsion energy as obtained from Psi4.
        """
        return self._nuclear_repulsion_eng

    @property
    def transform_eng_shift(self):
        """
        Energy shifted caused by active space transformation. This value is
        added to the final result to compensate for
        it.
        """
        return self._transform_eng_shift

    @property
    def full_ham_one_body_integrals_ao(self):
        """
        1-body electronic integrals of the full (non-transformed)
        Hamiltonian in the atomic basis.
        """
        return self._full_ham_one_body_integrals_ao

    @property
    def full_ham_two_body_integrals_ao(self):
        """
        2-body electronic integrals of the full (non-transformed)
        Hamiltonian in the atomic basis.
        """
        return self._full_ham_two_body_integrals_ao

    @property
    def full_ham_one_body_integrals_mo(self):
        """
        1-body electronic integrals of the full (non-transformed)
        Hamiltonian in the molecular basis.
        """
        return self._full_ham_one_body_integrals_mo

    @full_ham_one_body_integrals_mo.setter
    def full_ham_one_body_integrals_mo(self, ints):
        """
        The setter for 1-body electronic integrals of the full (non-transformed)
        Hamiltonian in the molecular basis.
        """
        self._full_ham_one_body_integrals_mo = ints

    @property
    def full_ham_two_body_integrals_mo(self):
        """
        2-body electronic integrals of the full (non-transformed)
        Hamiltonian in the molecular basis.
        """
        return self._full_ham_two_body_integrals_mo

    @full_ham_two_body_integrals_mo.setter
    def full_ham_two_body_integrals_mo(self, ints):
        """
        The setter for 1-body electronic integrals of the full (non-transformed)
        Hamiltonian in the molecular basis.
        """
        self._full_ham_two_body_integrals_mo = ints

    @property
    def one_body_el_int_nuc_der(self):
        """
        Nuclear derivatives of 1-body electronic integrals in the molecular
        basis.
        """
        return self._one_body_el_int_nuc_der

    @property
    def two_body_el_int_nuc_der(self):
        """
        Nuclear derivatives of 2-body electronic integrals in the molecular
        basis.
        """
        return self._two_body_el_int_nuc_der

    def update_problem_from_mo_coeffs(self, c: np.array):
        """
        Updates Hamiltonian with electronic integrals, basis transformer and
        matrix of molecular-orbital coefficients.
        If the integrals are passed in atomic orbital basis, they will be
        transformed to the molecular one using 'c'
        matrix.

        :param c: Matrix of molecular orbital coefficients.
        """

        # TODO account for other than alpha-spin orbitals too!

        self._c_mat = c

        # Create new BasisTransformer with MO coefficients
        self._basis_transformer = BasisTransformer(
            ElectronicBasis.AO,
            ElectronicBasis.MO,
            ElectronicIntegrals.from_raw_integrals(c),
        )

        # Recompute MO electronic integrals via transformation from AO
        # integrals obtained by Psi4
        # TODO Do NOT account only for 'alpha' spin!!!
        new_ints = self._basis_transformer.transform_electronic_integrals(
            self._full_ham_ao_integrals
        )
        self._full_ham_one_body_integrals_mo = new_ints.one_body.alpha["+-"]
        self._full_ham_two_body_integrals_mo = new_ints.two_body.alpha["++--"]

        # Construct new Hamiltonian and transform it via active space
        new_ham = ElectronicEnergy.from_raw_integrals(
            self._full_ham_one_body_integrals_mo, self._full_ham_two_body_integrals_mo
        )
        # self._full_ops[0] = new_ham.second_q_op()
        # self._second_q_full_ham_op = self._full_ops[0]
        self._as_ops[0] = self._active_space_transformer.transform_hamiltonian(
            new_ham
        ).second_q_op()
        self._second_q_active_ham_op = self._as_ops[0]

        # Recompute a constant shift caused by active-space transformation
        self._transform_eng_shift = 0
        for i in self.frozen_orbitals_indices:
            self._transform_eng_shift += 2 * self._full_ham_one_body_integrals_mo[i, i]
            for j in self.frozen_orbitals_indices:
                self._transform_eng_shift += (
                    2 * self._full_ham_two_body_integrals_mo[i, j, j, i]
                    - self._full_ham_two_body_integrals_mo[i, j, i, j]
                )

        # TODO only for debug
        # TODO remove constant terms from Hamiltonian itself later - only
        #  add it to results to mitigate noise!
        tmp = self._second_q_active_ham_op._data.copy()
        tmp[""] = self.nuclear_repulsion_eng + self.transform_eng_shift
        test = FermionicOp(tmp, num_spin_orbitals=self._as_problem.num_spin_orbitals)
        self._second_q_active_ham_op = test

        self._qubit_active_hamiltonian = self._fermionic_mapper.map(
            self._second_q_active_ham_op
        )

    def create_1_body_exc_op_active(self):
        """
        Creates 1-body excitation operator in the active space.
        """
        n_act_mo = self.n_orbitals_active
        self._one_body_exc_op_active = [
            [
                FermionicOp(
                    {
                        f"+_{p + spin * n_act_mo} -_{q + spin * n_act_mo}": 1
                        for spin in (0, 1)
                    },
                    num_spin_orbitals=self.as_problem.num_spin_orbitals,
                )
                for q in range(n_act_mo)
            ]
            for p in range(n_act_mo)
        ]

    def create_1_body_exc_op_full(self):
        """
        Creates 1-body excitation operator in the full space (without
        active-space transformation).
        """
        n_mo = self.n_molecular_orbitals
        self._one_body_exc_op_full = [
            [
                FermionicOp(
                    {f"+_{p + spin * n_mo} -_{q + spin * n_mo}": 1 for spin in (0, 1)},
                    num_spin_orbitals=self.full_problem.num_spin_orbitals,
                )
                for q in range(n_mo)
            ]
            for p in range(n_mo)
        ]

    def create_2_body_exc_op_active(self):
        """
        Creates 2-body excitation operator in the active space.
        """
        n_act_mo = self.n_orbitals_active
        self._two_body_exc_op_active = [
            [
                [
                    [
                        FermionicOp(
                            {
                                f"+_{p + spin1 * n_act_mo} +_{r + spin2 * n_act_mo} "
                                f"-_{s + spin2 * n_act_mo} -_{q + spin1 * n_act_mo}": 1
                                for spin1 in (0, 1)
                                for spin2 in (0, 1)
                            },
                            num_spin_orbitals=self.as_problem.num_spin_orbitals,
                        )
                        for s in range(n_act_mo)
                    ]
                    for r in range(n_act_mo)
                ]
                for q in range(n_act_mo)
            ]
            for p in range(n_act_mo)
        ]

    def create_2_body_exc_op_full(self):
        """
        Creates 2-body excitation operator in the full space (without
        active-space transformation).
        """
        n_mo = self.n_molecular_orbitals
        self._two_body_exc_op_full = [
            [
                [
                    [
                        FermionicOp(
                            {
                                f"+_{p + spin1 * n_mo} +_{r + spin2 * n_mo} "
                                f"-_{s + spin2 * n_mo} -_{q + spin1 * n_mo}": 1
                                for spin1 in (0, 1)
                                for spin2 in (0, 1)
                            },
                            num_spin_orbitals=self.full_problem.num_spin_orbitals,
                        )
                        for s in range(n_mo)
                    ]
                    for r in range(n_mo)
                ]
                for q in range(n_mo)
            ]
            for p in range(n_mo)
        ]

    def get_qubit_hamiltonian_nuclear_derivative_op(
        self, atom_moved: int
    ) -> list[Optional[Union[SparsePauliOp]]]:
        """
        Obtain the nuclear derivative Hamiltonian operator in the active space.

        :param atom_moved: Index of the atom w.r.t. which coordinates the
            nuclear derivatives are computed.
        :return: Nuclear derivative Hamiltonian operator.
        """
        if None in self._qubit_ham_nuc_deriv_op[atom_moved]:
            self.construct_hamiltonian_nuc_deriv_op(atom_moved)
        return self._qubit_ham_nuc_deriv_op[atom_moved]

    def _get_active_space_integrals(
        self,
        one_body_integrals,
        two_body_integrals,
        frozen_orb_idxs=None,
        active_orb_idxs=None,
    ):
        frozen_orb_idxs = [] if frozen_orb_idxs is None else frozen_orb_idxs
        if len(active_orb_idxs) < 1:
            raise ValueError("Some active indices required for reduction.")

        # Determine core constant
        core_constant = [0.0] * 3
        one_body_integrals_new = np.copy(one_body_integrals)

        for idx in range(3):
            for i in frozen_orb_idxs:
                core_constant[idx] += 2 * one_body_integrals[idx][i, i]
                for j in frozen_orb_idxs:
                    core_constant[idx] += (
                        2 * two_body_integrals[idx][i, i, j, j]
                        - two_body_integrals[idx][i, j, i, j]
                    )

            for u in active_orb_idxs:
                for v in active_orb_idxs:
                    for i in frozen_orb_idxs:
                        one_body_integrals_new[idx][u, v] += (
                            2 * two_body_integrals[idx][i, i, v, u]
                            - two_body_integrals[idx][i, v, i, u]
                        )

        return (
            core_constant,
            [
                e[np.ix_(active_orb_idxs, active_orb_idxs)]
                for e in one_body_integrals_new
            ],
            [
                e[
                    np.ix_(
                        active_orb_idxs,
                        active_orb_idxs,
                        active_orb_idxs,
                        active_orb_idxs,
                    )
                ]
                for e in two_body_integrals
            ],
        )

    def construct_hamiltonian_nuc_deriv_op(self, atom_moved: int) -> None:
        """
        Construct Hamiltonian nuclear derivatives operator and evaluate it for the given atom coordinates.

        :param atom_moved: Index of the atom w.r.t. which coordinates the
            nuclear derivatives are computed.
        """

        # Construct explicit terms in molecular-orbital basis
        explicit_terms = self._get_explicit_ham_deriv_terms(atom_moved)
        self._enuc_deriv[atom_moved] = explicit_terms["enuc_deriv"]
        self._ao_overlap_el_int_nuc_der_explicit[atom_moved] = explicit_terms[
            "ao_overlap_deriv"
        ]
        self._ao_one_body_el_int_nuc_der_explicit[atom_moved] = explicit_terms[
            "ao1_deriv"
        ]
        self._ao_two_body_el_int_nuc_der_explicit[atom_moved] = explicit_terms[
            "ao2_deriv"
        ]
        self._mo_overlap_el_int_nuc_der_explicit[atom_moved] = explicit_terms[
            "mo_overlap_deriv"
        ]
        self._mo_one_body_el_int_nuc_der_explicit[atom_moved] = explicit_terms[
            "mo1_deriv"
        ]
        self._mo_two_body_el_int_nuc_der_explicit[atom_moved] = explicit_terms[
            "mo2_deriv"
        ]

        # Obtain nuclear derivatives of 1- and 2-body integrals in
        # electronic Hamiltonian
        #   Paper notation: \frac{\partial h_{pq}}{\partial x},
        #   \frac{\partial g_{pqrs}}{\partial x}
        core_adjustment = None
        if (
            self._one_body_el_int_nuc_der[atom_moved] is None
            or self._two_body_el_int_nuc_der[atom_moved] is None
        ):
            (
                self._one_body_el_int_nuc_der[atom_moved],
                self._two_body_el_int_nuc_der[atom_moved],
            ) = self._get_ham_int_nuc_derivs(
                self._mo_overlap_el_int_nuc_der_explicit[atom_moved],
                self._mo_one_body_el_int_nuc_der_explicit[atom_moved],
                self._mo_two_body_el_int_nuc_der_explicit[atom_moved],
                self._full_ham_one_body_integrals_mo,
                self._full_ham_two_body_integrals_mo,
            )

            # Restrict nuclear derivatives of the integrals to the active space
            (
                core_adjustment,
                self._one_body_el_int_nuc_der_transformed[atom_moved],
                self._two_body_el_int_nuc_der_transformed[atom_moved],
            ) = self._get_active_space_integrals(
                self._one_body_el_int_nuc_der[atom_moved],
                self.two_body_el_int_nuc_der[atom_moved],
                self._frozen_orbitals_indices,
                self._active_orbitals,
            )

        # Create fermionic operators
        for i in range(3):
            # Create operator without a constant term
            # TODO rewrite in a way, that constant term is separated from
            #  the operator itself
            tmp = ElectronicEnergy.from_raw_integrals(
                h1_a=self._one_body_el_int_nuc_der_transformed[atom_moved][i],
                h2_aa=self._two_body_el_int_nuc_der_transformed[atom_moved][i],
                auto_index_order=False,
            ).second_q_op()

            # Create an operator with a constant term added
            tmp._data[""] = self._enuc_deriv[atom_moved][i] + core_adjustment[i]

            self._second_q_ham_nuc_deriv_op[atom_moved][i] = tmp

        # Create an operator consisting of Pauli strings
        self._qubit_ham_nuc_deriv_op[atom_moved] = tuple(
            self._fermionic_mapper.map(self._second_q_ham_nuc_deriv_op[atom_moved][i])
            for i in range(3)
        )

    def _get_explicit_ham_deriv_terms(self, atom_moved):
        r"""
        Derivatives of 1- and 2-body integrals in atomic-orbital basis set
          Paper notation: \frac{\partial S_{\mu \nu}}{\partial x},
          \frac{\partial h_{\mu \nu}}{\partial x},
                          \frac{\partial g_{\mu \nu \delta \gamma}}{\partial x}
        """

        # Explicit terms in atomic basis
        #   Paper notation: S^{(x)}_{pq}, h^{(x)}_{pq}, g^{(x)}_{pqrs}
        # TODO remove redundant SCF call, if it's possible to extract these
        #  objects from "general" Qiskit interface
        if not self._psi4_mints:
            if not self._psi4_wfn:
                psi4.core.clean()
                psi4.core.clean_variables()
                psi4.core.clean_options()
                psi4.set_options(
                    {"basis": self.basis_name, "reference": "rhf", "SCF_TYPE": "pk"}
                )
                psi4.core.set_output_file("psi4-rhf.out", append=False)
                _, self._psi4_wfn = psi4.energy(
                    "HF",
                    molecule=self.molecule.psi4_molecule,
                    return_wfn=True,
                    verbose=0,
                )
                self._c_mat = np.array(self._psi4_wfn.Ca())
            self._psi4_mints = psi4.core.MintsHelper(self._psi4_wfn.basisset())

        # Derivative of nuclear repulsion energy
        #   Paper notation: \frac{\partial E_{nuc}}{\partial x}
        enuc_deriv = (
            self.molecule.psi4_molecule.nuclear_repulsion_energy_deriv1().np[
                atom_moved,
            ]
            / self._unit_constants["Bohr_to_Angstrom"]
        )

        # Derivative of AO-overlap integrals
        #   Paper notation: \frac{\partial S_{\mu \nu}}{\partial x}
        ao_overlap_deriv = np.array(
            self._psi4_mints.ao_oei_deriv1(oei_type="OVERLAP", atom=atom_moved)
        )

        # Derivative of AO 1-electron integrals
        #   Paper notation: \frac{\partial h_{\mu \nu}}{\partial x}
        ao1_deriv = np.array(
            self._psi4_mints.ao_oei_deriv1(oei_type="KINETIC", atom=atom_moved)
        ) + np.array(
            self._psi4_mints.ao_oei_deriv1(oei_type="POTENTIAL", atom=atom_moved)
        )

        # Derivative of AO 2-electron integrals
        #   Paper notation: \frac{\partial g_{\mu \nu \delta \gamma}}{
        #   \partial x}
        ao2_deriv = np.array(self._psi4_mints.ao_tei_deriv1(atom=atom_moved))

        ################################################################################
        # Matrices of derivatives of 1- and 2-body integrals in
        # molecular-orbital basis
        ################################################################################

        # Derivative of MO-overlap integrals
        #   Paper notation: \frac{\partial S^{(x)}_{pq}}{\partial x}
        mo_overlap_deriv = (
            np.array(
                [
                    self.general_basis_change(ao_overlap_deriv[i], (1, 0))
                    for i in range(3)
                ]
            )
            / self._unit_constants["Bohr_to_Angstrom"]
        )

        # Derivative of MO 1-electron integrals
        #   Paper notation: \frac{\partial h^{(x)}_{pq}}{\partial x}
        mo1_deriv = (
            np.array(
                [self.general_basis_change(ao1_deriv[i], (1, 0)) for i in range(3)]
            )
            / self._unit_constants["Bohr_to_Angstrom"]
        )

        # Derivative of MP 2-electron integrals
        #   Paper notation: \frac{\partial g^{(x)}_{pqrs}}{\partial x}
        mo2_deriv = (
            np.array(
                [
                    self.general_basis_change(ao2_deriv[i], (1, 1, 0, 0))
                    for i in range(3)
                ]
            )
            / self._unit_constants["Bohr_to_Angstrom"]
        )

        return {
            "enuc_deriv": enuc_deriv,
            "ao_overlap_deriv": ao_overlap_deriv,
            "ao1_deriv": ao1_deriv,
            "ao2_deriv": ao2_deriv,
            "mo_overlap_deriv": mo_overlap_deriv,
            "mo1_deriv": mo1_deriv,
            "mo2_deriv": mo2_deriv,
        }

    def _get_ham_int_nuc_derivs(
        self, mo_overlap_deriv, mo1_deriv, mo2_deriv, h_mo, g_mo
    ):
        # TODO optimize
        """
        Compute nuclear derivatives of integrals in Hamiltonian operator in
        molecular basis.

        :param mo_overlap_deriv:
        :param mo1_deriv:
        :param mo2_deriv:
        :param h_mo:
        :param g_mo:
        :return:
        :rtype:
        """

        # Number of molecular orbitals
        mo_num = self._n_molecular_orbitals
        h1 = 0
        h2 = 0
        g1, g2, g3, g4 = 0, 0, 0, 0

        # Copy parts of integral derivative matrices relevant w.r.t. the
        # chosen active space
        mo1_deriv_active = mo1_deriv.copy()
        mo2_deriv_active = mo2_deriv.copy()
        for p in range(mo_num):
            for q in range(mo_num):
                for m in range(mo_num):
                    h1 = h_mo[m, q]
                    h2 = h_mo[p, m]

                    mo1_deriv_active[0, p, q] -= 0.5 * (
                        mo_overlap_deriv[0, p, m] * h1 + mo_overlap_deriv[0, q, m] * h2
                    )
                    mo1_deriv_active[1, p, q] -= 0.5 * (
                        mo_overlap_deriv[1, p, m] * h1 + mo_overlap_deriv[1, q, m] * h2
                    )
                    mo1_deriv_active[2, p, q] -= 0.5 * (
                        mo_overlap_deriv[2, p, m] * h1 + mo_overlap_deriv[2, q, m] * h2
                    )

                    for s in range(mo_num):
                        for n in range(mo_num):
                            g1 = g_mo[n, s, m, q]
                            g2 = g_mo[p, s, m, n]
                            g3 = g_mo[p, s, n, q]
                            g4 = g_mo[p, n, m, q]
                            mo2_deriv_active[0, p, q, m, s] -= 0.5 * (
                                mo_overlap_deriv[0, p, n] * g1
                                + mo_overlap_deriv[0, q, n] * g2
                                + mo_overlap_deriv[0, m, n] * g3
                                + mo_overlap_deriv[0, s, n] * g4
                            )
                            mo2_deriv_active[1, p, q, m, s] -= 0.5 * (
                                mo_overlap_deriv[1, p, n] * g1
                                + mo_overlap_deriv[1, q, n] * g2
                                + mo_overlap_deriv[1, m, n] * g3
                                + mo_overlap_deriv[1, s, n] * g4
                            )
                            mo2_deriv_active[2, p, q, m, s] -= 0.5 * (
                                mo_overlap_deriv[2, p, n] * g1
                                + mo_overlap_deriv[2, q, n] * g2
                                + mo_overlap_deriv[2, m, n] * g3
                                + mo_overlap_deriv[2, s, n] * g4
                            )

        return mo1_deriv_active, mo2_deriv_active

    def general_basis_change(self, general_tensor, key, c_mat=None):
        r"""Change the basis of a general interaction tensor.
        Motivated by OpenFermion.
        """
        # TODO rewrite using BasisTransformer

        rotation_matrix = self._c_mat
        if c_mat is not None:
            rotation_matrix = c_mat

        # If operator acts on spin degrees of freedom, enlarge rotation matrix.
        n_orbitals = rotation_matrix.shape[0]
        if general_tensor.shape[0] == 2 * n_orbitals:
            rotation_matrix = np.kron(rotation_matrix, np.eye(2))

        order = len(key)

        # The 'abcd' part of the subscripts
        subscripts_first = "".join(chr(ord("a") + i) for i in range(order))

        # The 'Aa,Bb,Cc,Dd' part of the subscripts
        subscripts_rest = ",".join(
            chr(ord("a") + i) + chr(ord("A") + i) for i in range(order)
        )

        subscripts = subscripts_first + "," + subscripts_rest

        # The list of rotation matrices, conjugated as necessary.
        rotation_matrices = [
            rotation_matrix.conj() if x else rotation_matrix for x in key
        ]

        # "optimize = True" does greedy optimization, which will be enough
        # here.
        transformed_general_tensor = np.einsum(
            subscripts, general_tensor, *rotation_matrices, optimize=True
        )
        return transformed_general_tensor
