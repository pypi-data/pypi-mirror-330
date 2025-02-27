"""Module containing the core SAOOVQE engine.

Core SA-OO-VQE module comprising implementation of the core SA-OO-VQE solver
class together with optimizer interfaces etc. The module aims to contain
all the logic behind SA-OO-VQE solution, which is not directly connected to
the properties of the electronic structure problem being solved or to the
properties of logically-independent circuits
like an initial orthogonal set or an ansatz.
"""

from __future__ import annotations

import sys
import typing
from enum import auto, Enum
from typing import Union, Callable, Optional

import numpy as np
import scipy.linalg
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import BaseEstimator, BackendEstimatorV2, BackendEstimator
from qiskit.primitives import BaseEstimator, BaseEstimatorV2, BackendEstimatorV2, BackendEstimator, BaseSampler
from qiskit_algorithms.optimizers import Optimizer, SciPyOptimizer
from qiskit_ibm_runtime import EstimatorV2
from scipy.optimize import minimize_scalar
import psi4

from .circuits import OrthogonalCircuitSet, HermitianOperatorEvaluator
from .gradient import GradientEvaluator, GradMethod
from .logger_config import log
from .problem import ProblemSet

if typing.TYPE_CHECKING:
    from ansatz import Ansatz


class NoValueEnum(Enum):
    """
    Class specifying printing of enumerator elements.
    """

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}>"


class WeightAttribution(NoValueEnum):
    """
    The description of the state-weight attribution in the SA-OO-VQE method.
    The weights can be distributed equally or
    in a decreasing manner.
    """

    EQUIVALENT = auto()
    DECREASING = auto()


class UnivariateOptimizerMethod(str, Enum):
    """
    The enumerator denoting the set of supported univariate optimizers.
    """

    BRENT = "brent"
    BOUNDED = "bounded"
    GOLDEN = "golden"


class UnivariateOptimizer:
    """
    This class represents an object (method + numerical parameters)
    passable to scipy.optimize.minimize_scalar() function.

    SciPy Docs reference: https://docs.scipy.org/doc/scipy/reference
    /generated/scipy.optimize.minimize_scalar.html
    """

    def __init__(
            self,
            method: Union[
                Callable, UnivariateOptimizerMethod
            ] = UnivariateOptimizerMethod.BOUNDED,
            bracket: Optional[tuple[float] | list[float]] = None,
            bounds: Optional[tuple[float] | list[float]] = (0, 2 * np.pi),
            args: Optional[tuple] = None,
            tol: Optional[float] = None,
            options: Optional[dict] = None,
    ):
        self._method = method if callable(method) else method.name
        self._bracket = bracket
        self._bounds = bounds
        self._args = args
        self._tol = tol
        self._options = options if options else {"xatol": 1e-7}

    @property
    def method(self) -> Callable | UnivariateOptimizerMethod:
        """
        The univariate optimization method being used.
        """
        return self._method

    @property
    def bracket(self) -> Optional[tuple[float] | list[float]]:
        """
        The bracketing interval :math:`(a, b, c)` with :math:`a < b < c` or
        :math:`(a, c)`, for methods Brent
        and Golden. It serves as an initial interval, NOT limiting the
        location of an obtained solution.
        """
        return self._bracket

    @property
    def bounds(self) -> Optional[tuple[float] | list[float]]:
        """
        The bounds :math:`(a, b)` for Bounded method. This setting denotes
        its optimization domain.
        """
        return self._bounds

    @property
    def args(self) -> Optional[tuple]:
        """
        The set of extra parameters for the optimized function.
        """
        return self._args

    @property
    def tol(self) -> Optional[float]:
        """
        The termination threshold. Its behavior differs among solvers -
        check with the referenced SciPy documentation!
        """
        return self._tol

    @property
    def options(self) -> Optional[dict]:
        """
        The dictionary of solver-specific options.
        """
        return self._options


class SAOOVQE:
    """
    The SA-OO-VQE solver.

    This class comprises all the logic of the method except its
    logically-independent parts (e.g. ansatz) or the parts
    directly connected to the electronic structure properties.
    """

    def __init__(
            self,
            estimator: BackendEstimator | BackendEstimatorV2 | EstimatorV2,
            initial_circuits: OrthogonalCircuitSet,
            ansatz: Ansatz,
            problem: ProblemSet,
            sampler: BaseSampler = None,
            weight_attribution: WeightAttribution = WeightAttribution.EQUIVALENT,
            orbital_optimization_settings: Optional[dict] = None,
    ):
        # TODO make a univariate optimizer a passable parameter

        self._estimator = estimator
        self._sampler = sampler
        self._initial_circuits = initial_circuits
        self._ansatz = ansatz
        if isinstance(estimator, EstimatorV2):
            initial_circuits.transpile(estimator.session._backend)
            self._ansatz = transpile(ansatz, backend=estimator.session._backend)

        self._problem = problem
        self._n_states = len(self._initial_circuits)
        self._weights = self._weights_attribution(weight_attribution)

        # Evaluator for ACTIVE Hamiltonian
        transpiled_active_hamiltonian_evaluator = self._problem.qubit_active_hamiltonian.apply_layout(self._ansatz.layout)
        self._active_hamiltonian_evaluator = HermitianOperatorEvaluator(
            transpiled_active_hamiltonian_evaluator, self._estimator
        )

        # Evaluators for separated one- and two-body excitation operators
        # Initialized on-demand when computing gradients
        self._one_body_exc_op_evaluators: Union[
            list[list[HermitianOperatorEvaluator]], None
        ] = None
        self._two_body_exc_op_evaluators: Union[
            list[list[list[list[HermitianOperatorEvaluator]]]], None
        ] = None

        # TODO Is it possible to reuse Hamiltonian terms?
        transpiled_s_squared_evaluator = self._problem.qubit_s_squared.apply_layout(self._ansatz.layout)
        self._s_squared_evaluator = HermitianOperatorEvaluator(
            transpiled_s_squared_evaluator, self._estimator
        )

        # Evaluator for the sum of H and S2
        self._ham_s_squared_sum_evaluator = HermitianOperatorEvaluator(
            transpiled_active_hamiltonian_evaluator + transpiled_s_squared_evaluator,
            self._estimator
        )

        # Optimal ansatz parameters found by get_energy()
        self._ansatz_param_values = None

        # Optimal resolution angle found by get_energy()
        self._resolution_angle = None

        # Computed energies
        self._energies: Optional[np.ndarray] = None

        # Auxiliary variables to prevent their unnecessary re-computation
        # when computing gradients
        self._circuit_grad = None
        self._circuit_hess = None
        self._st_avg_circuit_hess = None
        self._n_orbital_multipliers = None
        self._cir_orb_hessian_avg = None
        self._cir_orb_hess_avg_filter = None
        self._orb_grads_filter = None
        self._orb_hessian_avg_filter = None
        self._cir_orb_hessians = None
        self._rdm1_eff = None
        self._rdm2_eff = None
        self._rdm_eff_avg = None
        self._x_eff_mats = None
        self._orb_multipliers_mat = None
        self._circ_multipliers = None

        # Auxiliary variables for computation of non-adiabatic couplings
        self._one_body_transition_matrix: Optional[np.ndarray] = None
        self._two_body_transition_matrix: Optional[np.ndarray] = None
        self._one_body_transition_matrix_eff: Optional[np.ndarray] = None
        self._two_body_transition_matrix_eff: Optional[np.ndarray] = None
        self._orb_grad_trans: Optional[np.ndarray] = None
        self._orb_grad_trans_filter: Optional[np.ndarray] = None
        self._orb_multipliers_mat_trans: Optional[np.ndarray] = None
        self._orb_multipliers_mat_trans_dHab: Optional[np.ndarray] = None
        self._cir_multipliers_trans: Optional[np.ndarray] = None
        self._cir_multipliers_trans_dHab: Optional[np.ndarray] = None
        self._rdm1_trans: Optional[np.ndarray] = None
        self._rdm2_trans: Optional[np.ndarray] = None
        self._tdm1_eff_trans: Optional[np.ndarray] = None
        self._tdm2_eff_trans: Optional[np.ndarray] = None
        self._x_eff_trans: Optional[np.ndarray] = None
        self._csf_nacs: list[np.ndarray | None] = [None] * self.problem.molecule.n_atoms
        self._ci_nacs: list[np.ndarray | None] = [None] * self.problem.molecule.n_atoms
        self._nacs: list[np.ndarray | None] = [None] * self.problem.molecule.n_atoms
        self._dHab: list[np.ndarray | None] = [None] * self.problem.molecule.n_atoms
        self._orb_multipliers_mat_trans_dHab: Optional[np.ndarray] = None
        self._cir_multipliers_trans_dHab: Optional[np.ndarray] = None

        # Circuits for computation of transition matrices
        #
        # Paper notation: |+^x\rangle and |+^y\rangle
        self._circ_trans_real: Optional[np.array] = None
        self._circ_trans_imag: Optional[np.array] = None

        # Already-computed Pauli chains expectation values
        self._pauli_exp_vals: dict[(str, QuantumCircuit), float] = {}

        # TODO check the parameters!!!
        self._gradient_evaluators: Union[None, list[GradientEvaluator]] = None

        # Expectation-value evaluators for Hamiltonian nuclear derivatives
        # w.r.t. different atoms
        self._ham_nuc_deriv_grad_evaluators = {
            i: {} for i in range(self._initial_circuits.n_states)
        }
        self._ham_nuc_deriv_grad_eval_funcs = {
            i: {} for i in range(self._initial_circuits.n_states)
        }

        self._ham_nuc_grads: Optional[list[list[np.ndarray]]] = [
                                                                    None
                                                                ] * self.problem.molecule.n_atoms

        # Variable containing a quantum circuit with the optimal resolution
        # angle and parametrized ansatz
        # For the purposes of derivative computations
        #
        # Initialized after the resolution angle is found
        self._parametrized_grad_circuits: Union[None, OrthogonalCircuitSet] = None

        # Circuits representing an optimalized state vectors
        # To be used for obtaining expectation values of single excited
        # operators etc.
        #
        # Initialized after both ansatz parameters and the resolution angle
        # are found.
        self._optimized_state_circuits: Union[None, list[QuantumCircuit]] = None

        # Reduced density matrices
        #
        # Paper notation: \gamma^I, \Gamma^I
        self._one_body_reduced_density_mats: Union[None, list[np.ndarray]] = None
        self._two_body_reduced_density_mats: Union[None, list[np.ndarray]] = None
        self._one_body_reduced_density_mat_avg: Union[None, np.ndarray] = None
        self._two_body_reduced_density_mat_avg: Union[None, np.ndarray] = None

        # Fock matrices
        #
        # Paper notation: F^I
        self._fock_mats: Union[None, list[np.ndarray]] = None
        self._fock_mat_avg: Union[None, np.ndarray] = None

        # Orbital gradients
        #
        # Paper notation: G^{O, I}
        self._orbital_gradients: Union[None, list[np.array]] = None
        self._orbital_gradient_avg: None | list[np.array] = None

        # Orbital Hessians
        # Paper notation: H^{OO, I}
        self._orbital_hessians: Union[None, list[np.array]] = None
        self._orbital_hessian_avg: Union[None, np.array] = None

        # Options for orbital optimization - if None, OO is not performed at
        # all
        self._orbital_optimization_settings: dict = orbital_optimization_settings

        # Number of optimized orbitals
        self._n_mo_optim: int = (
            self._orbital_optimization_settings.get(
                "n_mo_optim", self.problem.n_molecular_orbitals
            )
            if self._orbital_optimization_settings is not None
            else self.problem.n_molecular_orbitals
        )

        # Number of non-redundant orbital rotation parameters
        self._n_non_redundant_rotation_params: int = len(
            [
                (p, q)
                for q in range(self._n_mo_optim - 1)
                for p in range(q + 1, self._n_mo_optim)
                if not self._is_param_pair_redundant(p, q)
            ]
        )

        # Number of outer iterations (i.e. containing both SA-VQE and OO)
        self._n_total_iters: int = (
            self._orbital_optimization_settings.get("n_total_iters", 25)
            if self._orbital_optimization_settings is not None
            else 1
        )

        self._orb_opt_thresh: float = (
            self._orbital_optimization_settings.get("thresh", 1e-6)
            if self._orbital_optimization_settings is not None
            else None
        )

        log.info("SAOOVQE was created.")

    @property
    def orbital_optimization_settings(self) -> Optional[dict]:
        """
        The options of orbital-optimization process.
        """
        return self._orbital_optimization_settings

    @property
    def n_mo_optim(self) -> Optional[float]:
        """
        The number of optimized molecular orbitals.
        """

        return self._n_mo_optim

    @property
    def estimator(self) -> BaseEstimator:
        """
        The estimator object used to obtain expected values.
        """
        return self._estimator

    @property
    def initial_circuits(self) -> OrthogonalCircuitSet:
        """
        The set of circuits representing initial mutually orthogonal states.
        """
        return self._initial_circuits

    @property
    def ansatz(self) -> Ansatz:
        """
        The ansatz representing to-be-optimized part of a state vector.
        """
        return self._ansatz

    @property
    def problem(self) -> ProblemSet:
        """
        The electronic structure problem properties, relevant operators and
        the relevant methods.
        """
        return self._problem

    @property
    def weights(self) -> list[float]:
        """
        The weights corresponding to computed states.
        """
        return self._weights

    @property
    def active_hamiltonian_evaluator(self) -> HermitianOperatorEvaluator:
        """
        The expected-value estimator of Hamiltonian after active-space
        transformation.
        """
        return self._active_hamiltonian_evaluator

    @property
    def s_squared_evaluator(self) -> HermitianOperatorEvaluator:
        """
        The expected-value estimator of S^2 operator after active-space
        transformation.
        """
        return self._s_squared_evaluator

    @property
    def ansatz_param_values(self) -> Optional[np.ndarray]:
        """
        The optimal set of ansatz parameters after running
        :meth:`vqe_optimization.SAOOVQE.get_energy`.
        """
        return self._ansatz_param_values

    @property
    def resolution_angle(self) -> Optional[float]:
        """
        The optimal resolution angle in radians after running
        :meth:`vqe_optimization.SAOOVQE.get_energy`.
        """
        return self._resolution_angle

    @property
    def optimized_state_circuits(self) -> Optional[list[QuantumCircuit]]:
        """
        The set of circuits representing approximately-optimal state vectors
        obtained after running
        :meth:`vqe_optimization.SAOOVQE.get_energy`.
        """
        return self._optimized_state_circuits

    @property
    def dHab(self) -> list[np.ndarray | None]:
        """
        Derivative of H_AB = <Psi_A | H | Psi_B> coupling obtained by running :meth:`vqe_optimization.SAOOVQE.eval_dHab`.
        """
        return self._dHab

    @property
    def ci_nacs(self) -> list[np.ndarray | None]:
        """
        Non-adiabatic CI couplings obtained by running
        :meth:`vqe_optimization.SAOOVQE.eval_nac`.
        """
        return self._ci_nacs

    @property
    def csf_nacs(self) -> list[np.ndarray | None]:
        """
        Non-adiabatic CSF couplings obtained by running
        :meth:`vqe_optimization.SAOOVQE.eval_nac`.
        """
        return self._csf_nacs

    @property
    def total_nacs(self) -> list[np.ndarray | None]:
        """
        Total non-adiabatic (CI + CSF) couplings obtained by running
        :meth:`vqe_optimization.SAOOVQE.eval_nac`.
        """
        return self._nacs

    @property
    def rdms_1_body(self) -> None | list[np.ndarray]:
        """One-body reduced density matrices for all the involved states."""
        return self._one_body_reduced_density_mats

    @property
    def rdm_avg_1_body(self) -> None | np.ndarray:
        """Two-body average reduced density matrix for of all the involved states."""
        return self._one_body_reduced_density_mat_avg

    @property
    def rdms_2_body(self) -> None | list[np.ndarray]:
        """Two-body reduced density matrices for all the involved states."""
        return self._two_body_reduced_density_mats

    @property
    def rdm_avg_2_body(self) -> None | np.ndarray:
        """Two-body average reduced density matrix for of all the involved states."""
        return self._two_body_reduced_density_mat_avg

    def eval_state_overlap(self, circuit1: QuantumCircuit, circuit2: QuantumCircuit) -> float:
        """
        Measurement of state overlap utilizing Hadamard test.

        :param circuit1: The circuit representing the first state of the overlap
        :param circuit2: The circuit representing the second state of the overlap

        :return: The coefficient of the state overlap.
        """

        hadamard_test_circ = self._get_hadamard_test_circ(circuit1, circuit2)
        probs = self._sampler.run(hadamard_test_circ).result().quasi_dists[0]

        return probs.get(0, 0) - probs.get(1, 0)

    def eval_nac(self, atom_idx: int) -> np.array:
        """
        Computes non-adiabatic couplings for a given atom in a specific state.

        :param atom_idx: Index of the atom (with respect to the provided
            geometry), w.r.t. whose position the coupling is evaluated.
        :return: Vector of non-adiabatic couplings.
        """

        # Half derivatives of MO-basis overlap integrals
        c_mat_psi4 = psi4.core.Matrix.from_array(self.problem.c_mat)
        d_s_half_derivlf_deriv = (
                np.array(
                    self.problem.psi4_mints.mo_overlap_half_deriv1(
                        "LEFT", atom_idx, c_mat_psi4, c_mat_psi4
                    )
                )
                / self.problem.unit_constants["Bohr_to_Angstrom"]
        )

        if not self._parametrized_grad_circuits:
            raise RuntimeError(
                "Parametrized gradient circuits are NOT computed! "
                "Run get_energy() before eval_nac()."
            )

        if self._one_body_transition_matrix is None:
            self._compute_transition_matrix()

        # Compute state-averaged orbital gradient
        if self._orb_grad_trans_filter is None:
            self._orb_grad_trans = self._get_orbital_gradient_avg()
            self._orb_grad_trans_filter = self._reduce_orbital_gradient(
                self._orb_grad_trans
            )

        if self._cir_multipliers_trans is None or self._orb_multipliers_mat_trans is None:
            (
                self._orb_multipliers_mat_trans,
                self._cir_multipliers_trans,
            ) = self._get_lagrange_mults(
                np.zeros((self._n_states, len(self.ansatz_param_values))),
                [self._orb_grad_trans_filter],
            )

        if self._rdm1_trans is None or self._rdm2_trans is None:
            (
                self._rdm1_trans,
                self._rdm2_trans,
            ) = self._transform_rdms_with_orb_multipliers(
                self._one_body_reduced_density_mat_avg,
                self._two_body_reduced_density_mat_avg,
                self._orb_multipliers_mat_trans[0],
            )

        if self._tdm1_eff_trans is None or self._tdm2_eff_trans is None:
            self._tdm1_eff_trans = self._one_body_transition_matrix + self._rdm1_trans
            self._tdm2_eff_trans = self._two_body_transition_matrix + self._rdm2_trans

        if self._x_eff_trans is None:
            self._x_eff_trans = self._get_x_eff_i_matrix(
                self._tdm1_eff_trans,
                self._tdm2_eff_trans,
                self.problem.full_ham_one_body_integrals_mo,
                self.problem.full_ham_two_body_integrals_mo,
            )

        # Obtain CSF NACs
        nac_csf = -self._get_nac_csf(d_s_half_derivlf_deriv)
        self._csf_nacs[atom_idx] = nac_csf

        # Obtain CI NACs
        nac_ci = self._get_nac_ci(atom_idx)
        self._ci_nacs[atom_idx] = nac_ci

        # Total NACs
        self._nacs[atom_idx] = self._csf_nacs[atom_idx] + self._ci_nacs[atom_idx]

        return self._nacs[atom_idx]

    def eval_dHab(self, atom_idx: int) -> np.array:
        """
        Computes derivative of H_AB coupling for a given atom in a specific state.

        :param atom_idx: Index of the atom (with respect to the provided geometry),
                           w.r.t. whose position the coupling is evaluated.
        :return: Vector of dH_AB coupling.
        """
        if not self._parametrized_grad_circuits:
            raise RuntimeError('Parametrized gradient circuits are NOT computed! '
                               'Run get_energy() before eval_dHab().')

        if not self._gradient_evaluators:
            # self._construct_gradient_evaluators(self._ham_s_squared_sum_evaluator, self._parametrized_grad_circuits)

            # TODO is it necessary to evalute both gradients here? Or is it enough to construct ham_nuc_grad separately?
            self.eval_eng_gradient(0, atom_idx)
            self.eval_eng_gradient(1, atom_idx)

        # Compute circuit state-averaged Hessian
        #
        # Paper notation: H^{CC}
        if self._circuit_hess is None:
            self._circuit_hess = [
                e.eval_hess(self._ansatz_param_values)
                for e in self._gradient_evaluators
            ]

        if self._st_avg_circuit_hess is None:
            self._st_avg_circuit_hess = sum(
                w * h for w, h in zip(self.weights, self._circuit_hess)
            )

        # Compute state-averaged circuit-orbital Hessian
        #
        # Paper notation H^{CO}
        if self._cir_orb_hessians is None:
            (
                self._cir_orb_hessians,
                self._cir_orb_hessian_avg,
            ) = self._compute_circuit_orbital_hessians()

        # Reduce ("filter") orbital-dependent Hessians and gradient
        if self._orb_hessian_avg_filter is None:
            (
                self._orb_hessian_avg_filter,
                self._cir_orb_hess_avg_filter,
            ) = self._reduce_orbital_hessians(
                self._orbital_hessian_avg, self._cir_orb_hessian_avg
            )

        # Half derivatives of MO-basis overlap integrals
        c_mat_psi4 = psi4.core.Matrix.from_array(self.problem.c_mat)
        dS_half_deriv = np.array(self.problem._psi4_mints.mo_overlap_half_deriv1('LEFT',
                                                                                 atom_idx,
                                                                                 c_mat_psi4,
                                                                                 c_mat_psi4)) / self.problem.unit_constants['Bohr_to_Angstrom']

        if self._one_body_transition_matrix is None:
            self._compute_transition_matrix()

        # Compute state-averaged orbital gradient
        if self._orb_grad_trans_filter is None:
            self._orb_grad_trans = self._get_orbital_gradient_avg()
            self._orb_grad_trans_filter = self._reduce_orbital_gradient(self._orb_grad_trans)

        # Paper notation: G^{C, I}
        if self._circuit_grad is None:
            self._circuit_grad = np.array([e.eval_grad(self._ansatz_param_values) for e in self._gradient_evaluators])

        if self._cir_multipliers_trans_dHab is None:
            self._orb_multipliers_mat_trans_dHab, \
                self._cir_multipliers_trans_dHab = self._get_lagrange_mults(self._circuit_grad,
                                                                            [self._orb_grad_trans_filter])

        # Compute state-averaged orbital gradient
        if self._orb_grad_trans_filter is None:
            self._orb_grad_trans = self._get_orbital_gradient_avg()
            self._orb_grad_trans_filter = self._reduce_orbital_gradient(
                self._orb_grad_trans
            )

        if self._cir_multipliers_trans is None or self._orb_multipliers_mat_trans is None:
            (
                self._orb_multipliers_mat_trans,
                self._cir_multipliers_trans,
            ) = self._get_lagrange_mults(
                np.zeros((self._n_states, len(self.ansatz_param_values))),
                [self._orb_grad_trans_filter],
            )

        if self._rdm1_trans is None:
            self._rdm1_trans, \
                self._rdm2_trans = self._transform_rdms_with_orb_multipliers(self._one_body_reduced_density_mat_avg,
                                                                             self._two_body_reduced_density_mat_avg,
                                                                             self._orb_multipliers_mat_trans[0])

        if self._tdm1_eff_trans is None:
            self._tdm1_eff_trans = self._one_body_transition_matrix + self._rdm1_trans
            self._tdm2_eff_trans = self._two_body_transition_matrix + self._rdm2_trans

        if self._x_eff_trans is None:
            self._x_eff_trans = self._get_x_eff_i_matrix(self._tdm1_eff_trans,
                                                         self._tdm2_eff_trans,
                                                         self.problem.full_ham_one_body_integrals_mo,
                                                         self.problem.full_ham_two_body_integrals_mo)

        # Obtain dHab
        dHab = self._get_dHab(atom_idx)
        self._dHab[atom_idx] = dHab

        return self._dHab[atom_idx]

    def _get_orbital_gradient_avg(self):
        mat = np.zeros_like(self._one_body_transition_matrix)
        tdm1 = self._one_body_transition_matrix
        tdm2 = self._two_body_transition_matrix
        h = self.problem.full_ham_one_body_integrals_mo
        g = self.problem.full_ham_two_body_integrals_mo

        n_mo = h.shape[0]

        for p in range(n_mo):
            for q in range(n_mo):
                for r in range(n_mo):
                    mat[p, q] += (tdm1[p, r] + tdm1[r, p]) * h[q, r] - (
                            tdm1[q, r] + tdm1[r, q]
                    ) * h[p, r]
                    for s in range(n_mo):
                        for t in range(n_mo):
                            mat[p, q] += (tdm2[p, r, s, t] + tdm2[t, s, r, p]) * g[
                                q, t, s, r
                            ] - (tdm2[r, s, t, q] + tdm2[q, t, s, r]) * g[r, p, t, s]

        grad = np.zeros(self._n_mo_optim * (self._n_mo_optim - 1) // 2)
        for q in range(self._n_mo_optim - 1):
            for p in range(q + 1, self._n_mo_optim):
                grad[self._get_orbital_idx(p, q)] = mat[p, q]

        return grad

    def _get_nac_csf(self, ds_half_deriv):
        n_mo = ds_half_deriv[0].shape[0]
        nac_csf = np.zeros(3)

        for i in range(3):
            ds_dx_antisym = ds_half_deriv[i] - ds_half_deriv[i].conj().T
            for p in range(n_mo):
                for q in range(n_mo):
                    nac_csf[i] += 0.5 * (
                            self._one_body_transition_matrix[p, q] * ds_dx_antisym[p, q]
                    )

        return nac_csf

    def _get_nac_ci(self, atom_idx):
        n_mo = self.problem.one_body_el_int_nuc_der[atom_idx][0].shape[0]

        nac_ci = np.array(
            [
                self._cir_multipliers_trans[0]
                @ sum(
                    self.weights[sidx] * self._ham_nuc_grads[atom_idx][sidx][i]
                    for sidx in range(self._n_states)
                )
                for i in range(3)
            ]
        )

        for i in range(3):
            for p in range(n_mo):
                for q in range(n_mo):
                    nac_ci[i] += (
                            self.problem.one_body_el_int_nuc_der[atom_idx][i][p, q]
                            * self._tdm1_eff_trans[p, q]
                    )

                    for r in range(n_mo):
                        for s in range(n_mo):
                            nac_ci[i] += (
                                    0.5
                                    * self.problem.two_body_el_int_nuc_der[atom_idx][i][
                                        p, q, r, s
                                    ]
                                    * self._tdm2_eff_trans[p, q, r, s]
                            )

        return nac_ci / (self._energies[1] - self._energies[0])

    def _get_dHab(self, atom_idx):
        if (self.problem.one_body_el_int_nuc_der[atom_idx] is None
                or self.problem.two_body_el_int_nuc_der[atom_idx is None]):
            self.problem.construct_hamiltonian_nuc_deriv_op(atom_idx)

        n_mo = self.problem.one_body_el_int_nuc_der[atom_idx][0].shape[0]
        deriv_Hab = np.array([self._cir_multipliers_trans_dHab[0] @ sum(self.weights[sidx] * self._ham_nuc_grads[atom_idx][sidx][i]
                                                                        for sidx in range(self._n_states))
                              for i in range(3)])

        for i in range(3):
            for p in range(n_mo):
                for q in range(n_mo):
                    deriv_Hab[i] += self.problem.one_body_el_int_nuc_der[atom_idx][i][p, q] * self._tdm1_eff_trans[p, q]

                    for r in range(n_mo):
                        for s in range(n_mo):
                            deriv_Hab[i] += 0.5 * self.problem.two_body_el_int_nuc_der[atom_idx][i][p, q, r, s] * self._tdm2_eff_trans[p, q, r, s]

        return deriv_Hab

    def eval_eng_gradient(self, state_idx: int, atom_moved: int) -> np.ndarray:
        """
        Function to evaluate the energy gradient dE_{I}/dx.

        :param state_idx: Index I of the relevant state (0 - ground state,
            1 - first excited state)
        :param atom_moved: Index of the atom (with respect to the provided
            geometry), w.r.t. whose position the gradient is evaluated.
        :return: Energy gradient of the I-th state evaluated at the
            Cartesian coordinates of the selected atom.
        :rtype: tuple
        """

        # Check if necessary SAOOVQE properties are initialized
        if not self._gradient_evaluators:
            log.info("Constructing gradient evaluators...")
            if not self._parametrized_grad_circuits:
                raise RuntimeError(
                    "Parametrized gradient circuits are NOT computed! "
                    "Run get_energy() before eval_nac()."
                )
            self._construct_gradient_evaluators(
                self._ham_s_squared_sum_evaluator, self._parametrized_grad_circuits
            )

        # Compute circuit gradients
        #
        # Paper notation: G^{C, I}
        if self._circuit_grad is None:
            self._circuit_grad = np.array(
                [
                    e.eval_grad(self._ansatz_param_values)
                    for e in self._gradient_evaluators
                ]
            )

        # Compute circuit state-averaged Hessian
        #
        # Paper notation: H^{CC}
        if self._circuit_hess is None:
            self._circuit_hess = [
                e.eval_hess(self._ansatz_param_values)
                for e in self._gradient_evaluators
            ]

        if self._st_avg_circuit_hess is None:
            self._st_avg_circuit_hess = sum(
                w * h for w, h in zip(self.weights, self._circuit_hess)
            )

        # Prepare reduced-density matrices, if not already computed before
        if self._one_body_reduced_density_mat_avg is None:
            self.compute_rdms(self._optimized_state_circuits)

        if self._fock_mats is None:
            self._compute_fock_mats()

        # Compute orbital gradients
        #
        # Paper notation: G^{O, I}
        if self._orbital_gradients is None:
            self._compute_orbital_gradients()

        # Compute state-averaged orbital Hessian
        #
        # Paper notation H^{OO}
        if self._orbital_hessian_avg is None:
            self._compute_st_avg_orbital_hessian()

        # Compute state-averaged circuit-orbital Hessian
        #
        # Paper notation H^{CO}
        if self._cir_orb_hessians is None:
            (
                self._cir_orb_hessians,
                self._cir_orb_hessian_avg,
            ) = self._compute_circuit_orbital_hessians()

        # Reduce ("filter") orbital-dependent Hessians and gradient
        if self._orb_hessian_avg_filter is None:
            (
                self._orb_hessian_avg_filter,
                self._cir_orb_hess_avg_filter,
            ) = self._reduce_orbital_hessians(
                self._orbital_hessian_avg, self._cir_orb_hessian_avg
            )

        if self._orb_grads_filter is None:
            self._orb_grads_filter = [
                self._reduce_orbital_gradient(e) for e in self._orbital_gradients
            ]

            # Number of orbital Lagrange multipliers
            #
            # Paper notation: \kappa
            self._n_orbital_multipliers = len(self._orb_grads_filter[0])

        # Obtain Lagrange multipliers
        if self._circ_multipliers is None:
            (
                self._orb_multipliers_mat,
                self._circ_multipliers,
            ) = self._get_lagrange_mults(self._circuit_grad, self._orb_grads_filter)

        if self._rdm1_eff is None:
            # Transform state-average reduced-density matrices w.r.t. the
            # complete orbital multipliers
            #
            # Paper notation: \tilde{\gamma}
            tmp = [
                self._transform_rdms_with_orb_multipliers(
                    self._one_body_reduced_density_mat_avg,
                    self._two_body_reduced_density_mat_avg,
                    self._orb_multipliers_mat[i],
                )
                for i in range(self._n_states)
            ]

            rdm1s_transformed, rdm2s_transformed = zip(*tmp)

            # Efficient reduced-density matrix
            self._rdm1_eff = [
                self._one_body_reduced_density_mats[i] + rdm1s_transformed[i]
                for i in range(self._n_states)
            ]
            self._rdm2_eff = [
                self._two_body_reduced_density_mats[i] + rdm2s_transformed[i]
                for i in range(self._n_states)
            ]

        # Obtain Hamiltonian nuclear derivative
        #
        #   Paper notation: \frac{\partial H}{\partial x}

        # Obtain gradient of dH w.r.t. wavefunction parameters
        if atom_moved not in self._ham_nuc_deriv_grad_evaluators[state_idx]:
            for i in range(self._initial_circuits.n_states):
                self._construct_ham_nuc_deriv_grad_evaluators(atom_moved, i)

        # Obtain Hamiltonian nuclear gradients
        self._ham_nuc_grads[atom_moved] = np.array(
            [
                [
                    evaluator.eval_grad(self._ansatz_param_values)
                    for evaluator in self._ham_nuc_deriv_grad_evaluators[state][
                    atom_moved
                ]
                ]
                for state in self._ham_nuc_deriv_grad_evaluators
            ]
        )

        # Computation of the whole nuclear gradient
        #   Paper notation: \frac{\partial E_I}{\partial x}
        # TODO use list comprehension
        n_mo = self._problem.n_molecular_orbitals

        # Electron integral derivatives - explicit terms
        dhdx_explicit = self._problem.one_body_el_int_nuc_der_explicit_mo
        dgdx_explicit = self._problem.two_body_el_int_nuc_der_explicit_mo
        dsdx_explicit = self._problem.overlap_el_int_nuc_der_explicit_mo

        if self._x_eff_mats is None:
            self._x_eff_mats = [
                self._get_x_eff_i_matrix(
                    self._rdm1_eff[i],
                    self._rdm2_eff[i],
                    self.problem.full_ham_one_body_integrals_mo,
                    self.problem.full_ham_two_body_integrals_mo,
                )
                for i in range(self._n_states)
            ]

        grad_summed = np.array([0.0] * 3)

        for i in range(3):
            grad_summed[i] = self._problem.e_nuc_der[atom_moved][i] + (
                    self._circ_multipliers[state_idx]
                    @ sum(
                self.weights[sidx] * self._ham_nuc_grads[atom_moved][sidx][i]
                for sidx in range(self._n_states)
            )
            )

            for p in range(n_mo):
                for q in range(n_mo):
                    grad_summed[i] += (
                            dhdx_explicit[atom_moved][i][p, q]
                            * self._rdm1_eff[state_idx][p, q]
                            - self._x_eff_mats[state_idx][p, q]
                            * dsdx_explicit[atom_moved][i][p, q]
                    )
                    for r in range(n_mo):
                        for s in range(n_mo):
                            grad_summed[i] += (
                                    0.5
                                    * dgdx_explicit[atom_moved][i][p, q, r, s]
                                    * self._rdm2_eff[state_idx][p, q, r, s]
                            )
        return grad_summed

    def get_energy(
            self,
            st_avg_optimizer: Optimizer = SciPyOptimizer("BFGS"),
            angle_optimizer: UnivariateOptimizer = UnivariateOptimizer(),
            initial_ansatz_parameters: typing.List | np.ndarray = None,
            resolution_rotation: bool = True,
            s_squared_cost_coeff: float = 1,
            optim_thresh: float = 1e-8,
    ):
        """
        Extract the circuit-parameters, energies and states after the
        optimization of SA-VQE.

        Set resolution_rotation = False for diabatic calculations, for adiabatic leave True.
        """

        log.info("Computing energies...")

        # Extract the number of parameters from the ansatz and initialize
        # them to 0.
        #   Paper notation: theta
        # TODO more sophisticated initial guess?
        if initial_ansatz_parameters is not None:
            ansatz_params = initial_ansatz_parameters
        else:
            ansatz_params = np.zeros(self._ansatz.num_parameters)

        # Create circuits (ansatz + initial states) and obtain energy functions
        #   Paper notation: self._initial_circuits (PhiA, PhiB)
        #                   circuits (PsiA(theta), PsiB(theta))
        #   PsiA(theta) = Uhat|PhiA>
        #   PsiB(theta) = Uhat|PhiB>
        circuits = [c.compose(self._ansatz) for c in self._initial_circuits]

        # Paper notation: <PsiA(theta) | Hhat(kappa) | PsiA(theta)>, ...
        eng_funcs = self._get_eng_funcs(circuits)

        # Expectation values of S^2 operator to limit our focus to doublet
        # states
        s_squared_funcs = [
            self._s_squared_evaluator.get_evaluation_func(c) for c in circuits
        ]

        # Auxiliary circuit "to be rotated" after obtaining the
        # state-resolution rotation
        new_rotated_circuit = None

        # Energy functions after state-resolution rotation
        psi_circuit_eng_func = None

        # Optimization of ansatz parameters (\theta) and (optionally) of
        # molecular orbitals (\kappa)
        #
        # Note: Termination condition is in the end of the loop
        prev_cost = np.finfo(np.float64).max
        for i in range(self._n_total_iters):
            # Step 2: SA-VQE
            # Optimize the ansatz parameters THETA with respect to all the
            # considered states at once -
            # the set of parameters is common for all the ansatzes involved!
            #
            # State vectors involved: |psiA(theta)>, |psiB(theta)>
            optimization_res = st_avg_optimizer.minimize(
                lambda x: self._cost_function_state_averaged_energy(
                    x, eng_funcs, s_squared_funcs, s_squared_cost_coeff
                ),
                x0=ansatz_params,
            )

            # Paper notation: theta*
            self._ansatz_param_values = optimization_res.x

            log.info("SA-optimized ansatz parameters: %s", optimization_res.x)

            # Step 3:
            # Optimize kappa coefficients of Hamiltonian
            if self._orbital_optimization_settings is not None:
                log.info("Starting Orbital-Optimization process...")

                # Run Newton-Raphson to optimize Hamiltonian MO coefficients
                self.orb_opt_newton(
                    [c.assign_parameters(self._ansatz_param_values) for c in circuits]
                )

                # Renew functions for obtaining electronic energy with the
                # optimized Hamiltonian
                eng_funcs = self._get_eng_funcs(circuits)

            # Step 5: State-resolution procedure
            # Optimize phi angle to rotate both initial states in an optimal
            # way
            # TODO rewrite with help of SciPyOptimize class from Qiskit

            # 1) Create an "initial state to be rotated" |Phi0> = cos(
            # phi)|phiA> + sin(phi)|phiB>
            # TODO should get_new_rotation_circuit() be a method of initial
            #  circuits?
            new_rotated_circuit = self._initial_circuits.get_new_rotation_circuit()

            # 2) Apply U(theta*)
            #
            # Create U(theta*) by fixing theta* parameters
            utheta = self._ansatz.assign_parameters(
                {
                    param: self._ansatz_param_values[i]
                    for i, param in enumerate(self._ansatz.parameters)
                }
            )

            # Apply U(theta*)
            #   Paper notation: |Psi0(phi, theta*) = cos(phi)|PsiA(theta*)>
            #   + sin(phi)|PsiB(theta*)>
            psi_ground_circuit = new_rotated_circuit.compose(utheta)
            psi_circuit_eng_func = (
                self._active_hamiltonian_evaluator.get_evaluation_func(
                    psi_ground_circuit
                )
            )

            optim = self._cost_function_state_averaged_energy(
                self._ansatz_param_values,
                eng_funcs,
                s_squared_funcs,
                s_squared_cost_coeff,
            )
            # Termination condition on convergence
            if prev_cost - optim < optim_thresh:
                break
            prev_cost = optim

        # 3) Find optimal Phi
        #   Paper notation: phi*
        if resolution_rotation:
            res = minimize_scalar(
                lambda phi: psi_circuit_eng_func([phi]),
                method=angle_optimizer.method,
                bracket=angle_optimizer.bracket,
                bounds=angle_optimizer.bounds,
                tol=angle_optimizer.tol,
                options=angle_optimizer.options,
            )
            optimal_phi = res.x

            log.info(
                "Optimal phi angle for state-resolution was obtained (phi* = %s).",
                optimal_phi,
            )

        else:
            optimal_phi = 0

        # Assign found optimal values to the object properties
        self._resolution_angle = optimal_phi

        # Preparation of a circuit for derivative computations - for 1st
        # excited state add pi/2 to the input
        # TODO generalize for more than 2 states!
        # TODO make rotational angle and ansatz parameters class properties
        #  to enable lazy loading of them!
        # TODO doesn't belong to OrthogonalCircuitSet?
        self._parametrized_grad_circuits = [
            new_rotated_circuit.assign_parameters(
                (self._resolution_angle + rot,)
            ).compose(self._ansatz)
            for rot in (0, np.pi / 2)
        ]

        # Circuits representing an optimized state vectors
        #
        # To be used for obtaining expectation values of single excited
        # operators etc.
        self._optimized_state_circuits = [
            c.assign_parameters(self._ansatz_param_values)
            for i, c in enumerate(self._parametrized_grad_circuits)
        ]

        # Paper notation: <Psi0(phi*, theta*) | Hhat(kappa*) | Psi0(phi*,
        # theta*)>, ...
        self._energies = np.array(
            [
                psi_circuit_eng_func([self._resolution_angle]),
                psi_circuit_eng_func([self._resolution_angle + np.pi / 2]),
            ]
        )

        # Recompute RDMs with the optimized MO coefficients
        self.compute_rdms(self._optimized_state_circuits)

        return self._energies

    def orb_opt_newton(self, circuits):
        """
        Performs orbital-optimization process via Newton-Raphson method.
        """

        # Gradient termination threshold for Newton-Raphson
        grad_thresh = self._orb_opt_thresh

        # Maximum number of iterations
        max_iter = self._orbital_optimization_settings.get("max_iter", 25)

        # Check number of nonredundant rotation parameters
        n_nonredundant_params = sum(
            not self._is_param_pair_redundant(p, q)
            for p in range(self._n_mo_optim - 1)
            for q in range(p + 1, self._n_mo_optim)
        )

        if n_nonredundant_params == 0:
            raise RuntimeError(
                "Orbital-optimization unable to start, as all the rotation "
                "parameters are redundant! "
                "Raise number of optimized orbitals."
            )

        # Rotation vector
        k_vec = np.zeros((self._n_mo_optim * (self._n_mo_optim - 1) // 2, 1))

        # TODO do in a more sophisticated way
        eng_best = np.finfo(np.float64).max
        c_best = self.problem.c_mat

        # Build 1-body and 2-body RDMs from optimalized state circuits and a
        # generalized Fock matrix
        self.compute_rdms(circuits)

        for i in range(max_iter):
            log.info(f'Starting orbital optimization (iteration {i})')
            self._compute_st_avg_fock()
            self._compute_avg_orb_hess_grad_from_rdm()

            grad_avg_filter, hess_avg_filter = self._filter_orb_grad_hess(
                n_nonredundant_params
            )

            grad_norm = np.linalg.norm(grad_avg_filter)

            aug_hess = np.block(
                [
                    [0.0, grad_avg_filter],
                    [grad_avg_filter.reshape(-1, 1), hess_avg_filter],
                ]
            )
            _, aug_hess_eigvecs = np.linalg.eigh(aug_hess)

            step = np.reshape(
                aug_hess_eigvecs[1:, 0] / aug_hess_eigvecs[0, 0],
                np.shape(grad_avg_filter),
                )
            if np.max(np.abs(step)) > 5e-2:
                step = 5e-2 * step / np.max(np.abs(step))

            # Reshape 'step'
            step_reshaped = np.zeros(
                (self._n_mo_optim * (self._n_mo_optim - 1) // 2, 1)
            )
            idx_pq_filter = 0
            for p in range(self._n_mo_optim - 1):
                for q in range(p + 1, self._n_mo_optim):
                    idx_pq = self._get_orbital_idx(q, p)
                    if not self._is_param_pair_redundant(p, q):
                        step_reshaped[idx_pq] = step[idx_pq_filter]
                        idx_pq_filter += 1
            step = step_reshaped

            # Build rotation operator with Newton-Raphson step
            k_vec += step

            # Skew matrix (rotation generator)
            k_mat = self._transform_vec_to_skewmatrix(k_vec)

            # Rotation operator in MO basis (U = e^{-k_mat})
            u = scipy.linalg.expm(-k_mat).real

            # Completing the transformation operator
            #
            # In case not all the MOs are considered in the OO process,
            # the operator is extended with an identity block
            if self._n_mo_optim < self.problem.n_molecular_orbitals:
                u = scipy.linalg.block_diag(
                    u, np.eye(self.problem.n_molecular_orbitals - self._n_mo_optim)
                )

            # New MO coefficients matrix
            c_new = self._problem.c_mat @ u

            # Build new MOs
            # TODO Use BasisTransformer
            self.problem.full_ham_one_body_integrals_mo = (
                self.problem.general_basis_change(
                    self.problem.full_ham_one_body_integrals_ao, (1, 0), c_new
                )
            )
            self.problem.full_ham_two_body_integrals_mo = np.einsum(
                "pqrs->psrq",
                self.problem.general_basis_change(
                    self.problem.full_ham_two_body_integrals_ao, (1, 1, 0, 0), c_new
                ),
            )

            # Compute resulting energy after this OO iteration
            eng_new = self._energy_from_rdm()

            if eng_new < eng_best:
                eng_best = eng_new
                c_best = c_new

            log.info(f'Gradient norm: {grad_norm}')
            log.info(f'Energy after this OO iteration: {eng_new}')
            log.info(f'Best energy achieved: {eng_best}')

            if grad_norm < grad_thresh:
                break

        log.info('Orbital optimization was finished.')

        self.problem.update_problem_from_mo_coeffs(c_best)
        self._active_hamiltonian_evaluator = HermitianOperatorEvaluator(
            self._problem.qubit_active_hamiltonian, self._estimator
        )

        self._ham_s_squared_sum_evaluator = HermitianOperatorEvaluator(
            self._problem.qubit_active_hamiltonian + self._problem.qubit_s_squared,
            self._estimator,
            )

    def get_state_couplings(self, idx_a: int, idx_b: int) -> float:
        """
        This method computes interstate coupling :math:`\left< \psi_{a} | \hat{H} | \psi_{b} \right>`

        :param idx_a: Index of the first state that is used to compute the interstate coupling
        :param idx_b: Index of the second state that is used to compute the interstate coupling
        :return: Interstate coupling
        """

        if self._problem.full_ham_one_body_integrals_mo is None:
            raise RuntimeError('One-body integrals were not computed, run get_energy() first!')

        if self._one_body_transition_matrix is None:
            self._compute_transition_matrix()

        i_len, j_len, k_len, l_len = self._problem.full_ham_two_body_integrals_mo.shape
        res = 0

        for i in range(i_len):
            for j in range(j_len):
                res += self._problem.full_ham_one_body_integrals_mo[i, j] * self._one_body_transition_matrix[i, j]

                for k in range(k_len):
                    for l in range(k_len):
                        res += 0.5 * self._problem.full_ham_two_body_integrals_mo[i, l, k, j] * \
                               self._two_body_transition_matrix[i, j, k, l]

        return res

    def compute_rdms(self, circuits: list[QuantumCircuit] | OrthogonalCircuitSet):
        """
        This method computes both the one-body and two-body reduced density matrices.
        These matrices can be obtained via properties :meth:`saoovqe.vqe_optimization.SAOOVQE.rdms_1_body`,
        :meth:`saoovqe.vqe_optimization.SAOOVQE.rdms_2_body`, :meth:`saoovqe.vqe_optimization.SAOOVQE.rdm_avg_1_body`
        and :meth:`saoovqe.vqe_optimization.SAOOVQE.rdm_avg_2_body`.

        :param circuits: List of quantum circuits representing relevant states.
        """

        self._one_body_reduced_density_mats = [
            self._get_rdm1_from_idx(i, circuits) for i in range(len(circuits))
        ]

        self._two_body_reduced_density_mats = [
            self._get_rdm2_from_idx(i, self._one_body_reduced_density_mats[i], circuits)
            for i in range(len(circuits))
        ]

        self._one_body_reduced_density_mat_avg = sum(
            w * m for w, m in zip(self._weights, self._one_body_reduced_density_mats)
        )

        self._two_body_reduced_density_mat_avg = sum(
            w * m for w, m in zip(self._weights, self._two_body_reduced_density_mats)
        )

    def _eval_transition_amplitude(self, circ1, op, circ2):
        # TODO Re-use already-computed exp. values
        re = 0
        im = 0j
        for label, coeff in op.to_list():
            # Access the Pauli string label (primitive) and coefficient of
            # each term
            chain = label

            herm_estim = HermitianOperatorEvaluator(chain, self._estimator)

            for c in (self._circ_trans_real, circ1, circ2, self._circ_trans_imag):
                hc = id(c)
                if (chain, hc) not in self._pauli_exp_vals:
                    eval_f = herm_estim.get_evaluation_func(c)
                    self._pauli_exp_vals[(chain, hc)] = eval_f([])

            hc1 = id(circ1)
            hc2 = id(circ2)

            re += coeff * (
                    self._pauli_exp_vals[(chain, id(self._circ_trans_real))]
                    - 0.5
                    * (
                            self._pauli_exp_vals[(chain, hc1)]
                            + self._pauli_exp_vals[(chain, hc2)]
                    )
            )

            im += coeff * (
                    -self._pauli_exp_vals[(chain, id(self._circ_trans_imag))]
                    + 0.5
                    * (
                            self._pauli_exp_vals[(chain, hc1)]
                            + self._pauli_exp_vals[(chain, hc2)]
                    )
            )

        return re + 1j * im

    # TODO remove?
    def _hash_circ(self, circ):
        return str(circ.draw())

    def _get_lagrange_mults(self, cir_grads, orb_grads):
        system = np.block(
            [
                [self._orb_hessian_avg_filter, self._cir_orb_hess_avg_filter.T],
                [self._cir_orb_hess_avg_filter, self._st_avg_circuit_hess],
            ]
        )

        lagrange_mults = [
            np.linalg.solve(system, -np.concatenate((orb_grads[i], cir_grads[i])))
            for i in range(len(orb_grads))
        ]

        # Extract circuit multipliers
        #
        # Paper notation: \overline{\theta}
        circ_multipliers = [
            lagrange_mults[i][self._n_orbital_multipliers :]
            for i in range(len(orb_grads))
        ]

        # Extract orbital Lagrange multipliers and reconstruct them to the
        # original shape
        #
        # Paper notation: \overline{\kappa}
        orb_multipliers = [
            lagrange_mults[i][: self._n_orbital_multipliers]
            for i in range(len(orb_grads))
        ]
        orb_multipliers_mat = [
            self._reconstruct_orbital_lagrange_multipliers(orb_multipliers[i])
            for i in range(len(orb_grads))
        ]

        return orb_multipliers_mat, circ_multipliers

    def _compute_transition_matrix(self):
        r"""
        Computes a transition density matrix via the approached described in

        Nakanishi, K. M., Mitarai, K., & Fujii, K. (2019).
        Subspace-search variational quantum eigensolver for excited
        states. Physical Review Research, 1(3), 033062.

        Every real TDM inner product is determined via the identity

        .. math::
           \begin{align*}
               Re\left(\langle\Phi_i|\widehat{U}^\dagger(\theta^*)\widehat{
               A}\widehat{U}(\theta^*)|\Phi_j\rangle\right)
               &= \langle+^x_{ij}|\widehat{U}^\dagger(\theta^*)\widehat{
               A}\widehat{U}(\theta^*)|+^x_{ij} \rangle\\
               &= -\frac{1}{4} \langle\Phi_i|\widehat{U}^\dagger(
               \theta^*)\widehat{A}\widehat{U}(\theta^*)|\Phi_i\rangle
               \langle\Phi_j|\widehat{U}^\dagger(\theta^*)\widehat{
               A}\widehat{U}(\theta^*)|\Phi_j\rangle\\
               |+^x_{ij} \rangle &= \frac{|\Phi_i\rangle + |\Phi_j\rangle}{
               \sqrt{2}}\\
               |+^y_{ij} \rangle &= \frac{|\Phi_i\rangle + i|\Phi_j\rangle}{
               \sqrt{2}}
           \end{align*}
        """

        if self._circ_trans_real is None:
            self._assemble_auxiliary_trans_circuits()

        n_mo = self.problem.n_molecular_orbitals
        tdm1 = np.zeros((n_mo,) * 2)
        tdm2 = np.zeros((n_mo,) * 4)

        # # RDM elements at frozen space
        #  TODO maybe remove - always 0?
        # for i in self.problem.frozen_orbitals_indices:
        #     for j in self.problem.frozen_orbitals_indices:
        #         tdm1[i, j] = 2 * (i == j) * (sv0.conj() @ sv1).real
        #
        #         for k in self.problem.frozen_orbitals_indices:
        #             for l in self.problem.frozen_orbitals_indices:
        #                 tdm2[i, j, k, l] = (4 * (i == j) * (k == l) - 2 *
        #                 (i == l) * (j == k)) * (sv0.conj() @ sv1).real
        #

        for p_local, p in enumerate(self.problem.active_orbitals):
            for q_local, q in enumerate(self.problem.active_orbitals):
                tdm1[p, q] = self._eval_transition_amplitude(
                    self.optimized_state_circuits[0],
                    self.problem.fermionic_mapper.map(
                        self._problem.one_body_exc_op_active[p_local][q_local]
                    ),
                    self.optimized_state_circuits[1],
                ).real

                for r_local, r in enumerate(self.problem.active_orbitals):
                    for s_local, s in enumerate(self.problem.active_orbitals):
                        tdm2[p, q, r, s] = self._eval_transition_amplitude(
                            self.optimized_state_circuits[0],
                            self.problem.fermionic_mapper.map(
                                self._problem.two_body_exc_op_active[p_local][q_local][
                                    r_local
                                ][s_local]
                            ),
                            self.optimized_state_circuits[1],
                        ).real

                for i in self.problem.frozen_orbitals_indices:
                    for j in self.problem.frozen_orbitals_indices:
                        tdm2[i, j, p, q] = tdm2[p, q, i, j] = 2 * (i == j) * tdm1[p, q]
                        tdm2[p, i, j, q] = tdm2[j, q, p, i] = -(i == j) * tdm1[p, q]

        self._one_body_transition_matrix = tdm1
        self._two_body_transition_matrix = tdm2

    def _assemble_auxiliary_trans_circuits(self):
        """
        Assemble auxiliary quantum circuits to compute transition matrices.
        """

        # Prepare the ansatz filled with the optimal values
        ansatz_circ = self.ansatz.assign_parameters(self.ansatz_param_values)

        # Prepare an auxiliary circuit for the real part of an expectation
        # value
        self._circ_trans_real = QuantumCircuit(self.problem.n_qubits)
        self.initial_circuits.add_resolution_rotation_circuit(
            self._circ_trans_real, self._resolution_angle + np.pi / 4.0
        )
        self._circ_trans_real.compose(ansatz_circ, inplace=True)

        # Prepare an auxiliary circuit for the imaginary part of an
        # expectation value
        self._circ_trans_imag = self._create_trans_circ_imag(self._resolution_angle)
        self._circ_trans_imag.compose(ansatz_circ, inplace=True)

    def _create_trans_circ_imag(self, global_phase) -> QuantumCircuit:
        """
        Creates a circuit for computation of transition amplitude imaginary
        part.

        :param global_phase: Global phase of the circuit
        :return Quantum circuit for computation of the transition amplitude
        imaginary part.
        :rtype: QuantumCircuit
        """

        (n_alpha, n_beta) = self.initial_circuits.n_particles

        circuit = QuantumCircuit(self.problem.n_qubits, global_phase=-global_phase)

        # set all N-2 electrons in the lowest alpha- and beta-occupied
        # spin-orbitals
        for i in range(n_alpha - 1):
            circuit.x(i)
        for i in range(n_beta - 1):
            circuit.x(self.problem.n_qubits // 2 + i)

        circuit.ry(np.pi / 2, n_alpha - 1)
        circuit.x(self.problem.n_qubits // 2 + n_beta - 1)
        circuit.ch(n_alpha - 1, self.problem.n_qubits // 2 + n_beta)
        circuit.cx(
            self.problem.n_qubits // 2 + n_beta, self.problem.n_qubits // 2 + n_beta - 1
        )
        circuit.cx(self.problem.n_qubits // 2 + n_beta, n_alpha - 1)
        circuit.cx(n_alpha - 1, n_alpha)
        circuit.x(n_alpha - 1)

        # TODO check S-gate placement for more than 4 qubits!
        circuit.s(n_alpha)
        circuit.s(self.problem.n_qubits // 2 + n_beta)

        return circuit

    def _compute_avg_orb_hess_grad_from_rdm(self):
        """
        Compute state-averaged orbital gradient and Hessian using already
        computed state-average RDMs and state-average
        Fock matrix.
        """

        rdm1_avg = self._one_body_reduced_density_mat_avg
        rdm2_avg = self._two_body_reduced_density_mat_avg
        fock_avg = self._fock_mat_avg
        h_mo = self.problem.full_ham_one_body_integrals_mo
        g_mo = self.problem.full_ham_two_body_integrals_mo
        grad_avg = np.zeros(self._n_mo_optim * (self._n_mo_optim - 1) // 2)
        hess_avg = np.zeros((self._n_mo_optim * (self._n_mo_optim - 1) // 2,) * 2)
        orb_indices = (
                self.problem.frozen_orbitals_indices + self.problem.active_orbitals
        )

        # TODO optimize with 'prange'!!!
        for q in range(self._n_mo_optim - 1):
            for p in range(q + 1, self._n_mo_optim):
                ind_pq = self._get_orbital_idx(p, q)

                # Computing the gradient vector elements
                grad_avg[ind_pq] = 2.0 * (
                        self._fock_mat_avg[p, q] - self._fock_mat_avg[q, p]
                )

                # Continue the loop to compute the hessian matrix elements
                for s in range(self._n_mo_optim - 1):
                    for r in range(s + 1, self._n_mo_optim):
                        ind_rs = self._get_orbital_idx(r, s)

                        hess_avg[ind_pq, ind_rs] = (
                                (
                                        (fock_avg[p, s] + fock_avg[s, p]) * (q == r)
                                        - 2.0 * h_mo[p, s] * rdm1_avg[q, r]
                                )
                                - (
                                        (fock_avg[q, s] + fock_avg[s, q]) * (p == r)
                                        - 2.0 * h_mo[q, s] * rdm1_avg[p, r]
                                )
                                - (
                                        (fock_avg[p, r] + fock_avg[r, p]) * (q == s)
                                        - 2.0 * h_mo[p, r] * rdm1_avg[q, s]
                                )
                                + (
                                        (fock_avg[q, r] + fock_avg[r, q]) * (p == s)
                                        - 2.0 * h_mo[q, r] * rdm1_avg[p, s]
                                )
                        )

                        for u in orb_indices:
                            for v in orb_indices:
                                hess_avg[ind_pq, ind_rs] += (
                                        (
                                                2
                                                * g_mo[p, v, r, u]
                                                * (rdm2_avg[q, u, s, v] + rdm2_avg[q, u, v, s])
                                                + 2 * g_mo[p, v, u, r] * rdm2_avg[q, s, u, v]
                                        )
                                        - (
                                                2
                                                * g_mo[q, v, r, u]
                                                * (rdm2_avg[p, u, s, v] + rdm2_avg[p, u, v, s])
                                                + 2 * g_mo[q, v, u, r] * rdm2_avg[p, s, u, v]
                                        )
                                        - (
                                                2
                                                * g_mo[p, v, s, u]
                                                * (rdm2_avg[q, u, r, v] + rdm2_avg[q, u, v, r])
                                                + 2 * g_mo[p, v, u, s] * rdm2_avg[q, r, u, v]
                                        )
                                        + (
                                                2
                                                * g_mo[q, v, s, u]
                                                * (rdm2_avg[p, u, r, v] + rdm2_avg[p, u, v, r])
                                                + 2 * g_mo[q, v, u, s] * rdm2_avg[p, r, u, v]
                                        )
                                )

        self._orbital_hessian_avg = hess_avg
        self._orbital_gradient_avg = grad_avg

    def _filter_orb_grad_hess(
            self, n_nonredundant_params: int
    ) -> tuple[np.array, np.array]:
        """
        Filters orbital gradients and Hessians w.r.t. active, frozen and
        virtual indices, so that only non-redundant
        will remain.

        :return: Filtered gradient and Hessian
        :rtype: tuple[np.array, np.array]
        """

        grad_filter = np.zeros(n_nonredundant_params)
        hess_filter = np.zeros((n_nonredundant_params,) * 2)

        idx_pq_filter = 0
        for p in range(self._n_mo_optim - 1):
            for q in range(p + 1, self._n_mo_optim):
                if not self._is_param_pair_redundant(p, q):
                    idx_pq = self._get_orbital_idx(q, p)
                    grad_filter[idx_pq_filter] = self._orbital_gradient_avg[idx_pq]

                    idx_rs_filter = 0
                    for r in range(self._n_mo_optim - 1):
                        for s in range(r + 1, self._n_mo_optim):
                            if not self._is_param_pair_redundant(r, s):
                                idx_rs = self._get_orbital_idx(s, r)

                                hess_filter[
                                    idx_pq_filter, idx_rs_filter
                                ] = self._orbital_hessian_avg[idx_pq, idx_rs]
                                idx_rs_filter += 1
                    idx_pq_filter += 1

        return grad_filter, hess_filter

    def _energy_from_rdm(self) -> float:
        """
        Computes energy in an efficient way without need for measurements
        utilizing reduced density matrices and
        electron integrals.

        :return: System energy w.r.t. current RDMs and electron integrals
        :rtype: float
        """
        n_orbs = len(self.problem.frozen_orbitals_indices) + len(
            self.problem.active_orbitals
        )
        energy = self.problem.nuclear_repulsion_eng
        for p in range(n_orbs):
            for q in range(n_orbs):
                energy += (
                        self._one_body_reduced_density_mat_avg[p, q]
                        * self.problem.full_ham_one_body_integrals_mo[p, q]
                )
                for r in range(n_orbs):
                    for s in range(n_orbs):
                        energy += (
                                0.5
                                * self._two_body_reduced_density_mat_avg[p, q, r, s]
                                * self.problem.full_ham_two_body_integrals_mo[p, s, r, q]
                        )
        return energy

    def _get_x_eff_i_matrix(
            self, rdm1_eff_st_spec, rdm2_eff_st_spec, dhdx_explicit, dgdx_explicit
    ):
        # TODO improve method name
        # TODO rewrite method + docs
        """
        Function to build the generalized Fock matrix associated to a given
        reference state |Psi_I> necessary in the  CP-MCSCF theory. Note that
        there is no evident simplifications made on the matrix contrary to
        the case of the Orb. Opt. process.
        """

        x_eff_i = np.zeros_like(rdm1_eff_st_spec)
        n_mo = np.shape(dhdx_explicit)[0]
        for p in range(n_mo):
            for q in range(n_mo):
                for r in range(n_mo):
                    x_eff_i[p, q] += rdm1_eff_st_spec[p, r] * dhdx_explicit[q, r]
                    for s in range(n_mo):
                        for t in range(n_mo):
                            x_eff_i[p, q] += (
                                    rdm2_eff_st_spec[p, r, s, t] * dgdx_explicit[q, t, s, r]
                            )
        return x_eff_i

    def _transform_rdms_with_orb_multipliers(self, rdm1_sa, rdm2_sa, orb_multipliers):
        rdm1_transformed = np.zeros_like(rdm1_sa)
        rdm2_transformed = np.zeros_like(rdm2_sa)
        n_mo = np.shape(rdm1_sa)[0]

        for p in range(n_mo):
            for q in range(n_mo):
                # Elements of the 1-RDM
                for m in range(n_mo):
                    # TODO In paper there is plus, but Saad has -
                    rdm1_transformed[p, q] += (
                            rdm1_sa[m, q] * orb_multipliers[m, p]
                            - rdm1_sa[p, m] * orb_multipliers[q, m]
                    )
                # Elements of the 2-RDM
                for r in range(n_mo):
                    for s in range(n_mo):
                        for n in range(n_mo):
                            rdm2_transformed[p, q, r, s] += (
                                    rdm2_sa[n, q, r, s] * orb_multipliers[n, p]
                                    + rdm2_sa[p, n, r, s] * orb_multipliers[n, q]
                                    + rdm2_sa[p, q, n, s] * orb_multipliers[n, r]
                                    + rdm2_sa[p, q, r, n] * orb_multipliers[n, s]
                            )

        return rdm1_transformed, rdm2_transformed

    def _transform_vec_to_skewmatrix(self, vec):
        """
        Function to build the skew-matrix - antisymmetric generator matrix K
        for
        the orbital rotations from a vector k.
        """
        k = np.zeros((self._n_mo_optim,) * 2)
        ind_ij = 0
        for j in range(self._n_mo_optim - 1):
            for i in range(j + 1, self._n_mo_optim):
                k[i, j] = vec[ind_ij].item()
                k[j, i] = -vec[ind_ij].item()
                ind_ij += 1
        return k

    def _reconstruct_orbital_lagrange_multipliers(self, reduced_multipliers):
        # Number of molecular orbitals
        n_mo = self._problem.n_molecular_orbitals
        n_mo_optim = self._n_mo_optim

        full_multipliers = np.zeros(n_mo_optim * (n_mo_optim - 1) // 2)
        ind_pq_filtered = 0
        for q in range(n_mo_optim - 1):
            for p in range(q + 1, n_mo_optim):
                if not self._is_param_pair_redundant(p, q):
                    ind_pq = self._get_orbital_idx(p, q)
                    full_multipliers[ind_pq] = reduced_multipliers[ind_pq_filtered]
                    ind_pq_filtered += 1

        # Build a matrix for the kappa_bar parameters (it facilitates the
        # future calculations )
        kappa_bar_matrix = np.block(
            [
                [
                    self._transform_vec_to_skewmatrix(full_multipliers),
                    np.zeros((n_mo_optim, n_mo - n_mo_optim)),
                ],
                [
                    np.zeros((n_mo_optim, n_mo - n_mo_optim)).T,
                    np.zeros((n_mo - n_mo_optim, n_mo - n_mo_optim)),
                ],
            ]
        )

        return kappa_bar_matrix

    def _is_param_pair_redundant(self, p, q):
        return any(
            all(e in lst for e in (p, q))
            for lst in (
                self._problem.frozen_orbitals_indices,
                self._problem.active_orbitals,
                self._problem.virtual_orbitals_indices,
            )
        )

    def _reduce_orbital_gradient(self, orbital_grad):
        orbital_grad_filtered = np.array(
            [
                orbital_grad[self._get_orbital_idx(p, q)]
                for q in range(self._n_mo_optim - 1)
                for p in range(q + 1, self._n_mo_optim)
                if not self._is_param_pair_redundant(p, q)
            ]
        )

        return orbital_grad_filtered

    def _reduce_orbital_hessians(self, orbital_hess, circuit_orbital_hess):
        # Number of non-redundant rotation parameters
        n_rot_params = self._n_non_redundant_rotation_params

        orbital_hess_filtered = np.zeros((n_rot_params, n_rot_params))
        circuit_orbital_hess_filtered = np.zeros(
            (self._ansatz.num_parameters, n_rot_params)
        )

        ind_pq_filtered = 0
        for q in range(self._n_mo_optim - 1):
            for p in range(q + 1, self._n_mo_optim):
                if not self._is_param_pair_redundant(p, q):
                    ind_pq = self._get_orbital_idx(p, q)

                    for i in range(self._ansatz.num_parameters):
                        circuit_orbital_hess_filtered[
                            i, ind_pq_filtered
                        ] = circuit_orbital_hess[i, ind_pq]

                    ind_rs_filtered = 0
                    for s in range(self._n_mo_optim - 1):
                        for r in range(s + 1, self._n_mo_optim):
                            if not self._is_param_pair_redundant(r, s):
                                ind_rs = self._get_orbital_idx(r, s)

                                # Orbital Hessian
                                orbital_hess_filtered[
                                    ind_pq_filtered, ind_rs_filtered
                                ] = orbital_hess[ind_pq, ind_rs]
                                ind_rs_filtered += 1

                    ind_pq_filtered += 1

        return orbital_hess_filtered, circuit_orbital_hess_filtered

    def _compute_circuit_orbital_hessians(self):
        # TODO parallel map?
        circuit_orbital_hessians = [
            self._get_circuit_orbital_hessian(i) for i in range(self._n_states)
        ]
        circuit_orbital_hessian_avg = sum(
            w * e for w, e in zip(self.weights, circuit_orbital_hessians)
        )

        return circuit_orbital_hessians, circuit_orbital_hessian_avg

    def _get_circuit_orbital_hessian(self, state_idx: int) -> np.array:
        # TODO rewrite as parameter shift???
        n_ansatz_params = self._ansatz.num_parameters

        # Delta for finite-differences approach
        d = 1e-5 / 2.0

        mat = np.zeros(
            (n_ansatz_params, self._n_mo_optim * (self._n_mo_optim - 1) // 2)
        )

        for i in range(n_ansatz_params):
            # Shift "+ delta"
            shifted_params_p = np.copy(self._ansatz_param_values)
            shifted_params_p[i] += d

            shift_circuit_p = self._parametrized_grad_circuits[
                state_idx
            ].assign_parameters(shifted_params_p)

            # Shift "- delta"
            shifted_params_m = np.copy(self._ansatz_param_values)
            shifted_params_m[i] -= d

            shift_circuit_m = self._parametrized_grad_circuits[
                state_idx
            ].assign_parameters(shifted_params_m)

            # Construct reduced-density matrices with shifted circuits
            rdm1_p = self._get_rdm1(shift_circuit_p)
            rdm1_m = self._get_rdm1(shift_circuit_m)
            rdm2_p = self._get_rdm2(shift_circuit_p, rdm1_p)
            rdm2_m = self._get_rdm2(shift_circuit_m, rdm1_m)

            # Construct Fock matrices
            for q in range(self._n_mo_optim - 1):
                for p in range(q + 1, self._n_mo_optim):
                    idx = self._get_orbital_idx(p, q)

                    fock_p = self._get_fock(rdm1_p, rdm2_p)
                    fock_m = self._get_fock(rdm1_m, rdm2_m)

                    grad_kappa_p = 2 * (fock_p[p, q] - fock_p[q, p])
                    grad_kappa_m = 2 * (fock_m[p, q] - fock_m[q, p])

                    mat[i, idx] = (grad_kappa_p - grad_kappa_m) / (2 * d)

        return mat

    def _get_orbital_idx(self, p, q):
        """
        Function returning a super-index used for G^O and H^{OO}, etc.
        """

        ini_int = self._n_mo_optim - 1 - q
        fin_int = self._n_mo_optim - 1
        counter = (fin_int - ini_int + 1) * (ini_int + fin_int) // 2
        ind_pq = counter + p - self._n_mo_optim
        return ind_pq

    def _compute_orbital_hessians(self):
        self._orbital_hessians = [
            self._get_orbital_hessian(i) for i in range(len(self._initial_circuits))
        ]

    def _compute_st_avg_orbital_hessian(self) -> np.array:
        # Hessian inner function
        in_fn = self._get_st_avg_orbital_hessian_inner_func

        hess = np.zeros(
            (
                (self._n_mo_optim * (self._n_mo_optim - 1) // 2),
                self._n_mo_optim * (self._n_mo_optim - 1) // 2,
            )
        )

        for q in range(self._n_mo_optim - 1):
            for p in range(q + 1, self._n_mo_optim):
                for s in range(self._n_mo_optim - 1):
                    for r in range(s + 1, self._n_mo_optim):
                        hess[
                            self._get_orbital_idx(p, q), self._get_orbital_idx(r, s)
                        ] = (
                                in_fn(p, q, r, s)
                                - in_fn(q, p, r, s)
                                - in_fn(p, q, s, r)
                                + in_fn(q, p, s, r)
                        )

        self._orbital_hessian_avg = hess

    def _get_orbital_hessian(self, state_idx: int) -> np.array:
        # Hessian inner function

        in_fn = self._get_st_spec_orbital_hessian_inner_func

        hess = np.zeros(
            (
                (self._n_mo_optim * (self._n_mo_optim - 1) // 2),
                self._n_mo_optim * (self._n_mo_optim - 1) // 2,
            )
        )

        for q in range(self._n_mo_optim):
            for p in range(self._n_mo_optim):
                for s in range(self._n_mo_optim):
                    for r in range(self._n_mo_optim):
                        hess[
                            self._get_orbital_idx(p, q), self._get_orbital_idx(r, s)
                        ] = (
                                in_fn(state_idx, p, q, r, s)
                                - in_fn(state_idx, q, p, r, s)
                                - in_fn(state_idx, p, q, s, r)
                                + in_fn(state_idx, q, p, s, r)
                        )
        return hess

    def _get_st_avg_orbital_hessian_inner_func(self, p, q, r, s):
        # Joined frozen and active orbitals
        relevant_orbs = (
                self._problem.frozen_orbitals_indices + self._problem.active_orbitals
        )

        f = self._fock_mat_avg
        delta = q == r
        h = self._problem.full_ham_one_body_integrals_mo
        gamma1 = self._one_body_reduced_density_mat_avg
        g = self._problem.full_ham_two_body_integrals_mo
        gamma2 = self._two_body_reduced_density_mat_avg

        inner_sum = sum(
            g[p, v, r, u] * (gamma2[q, u, s, v] + gamma2[q, u, v, s])
            + g[p, v, u, r] * gamma2[q, s, u, v]
            for v in relevant_orbs
            for u in relevant_orbs
        )

        return delta * (f[p, s] + f[s, p]) - 2 * h[p, s] * gamma1[q, r] + 2 * inner_sum

    def _get_st_spec_orbital_hessian_inner_func(self, state_idx, p, q, r, s):
        # TODO remove commented blocks of code
        # Joined frozen and active orbitals
        relevant_orbs = (
                self._problem.frozen_orbitals_indices + self._problem.active_orbitals
        )

        f = self._fock_mats[state_idx]
        delta = q == r
        h = self._problem.full_ham_one_body_integrals_mo
        gamma1 = self._one_body_reduced_density_mats[state_idx]
        g = self._problem.full_ham_two_body_integrals_mo
        gamma2 = self._two_body_reduced_density_mats[state_idx]

        inner_sum = sum(
            g[p, u, s, v] * (gamma2[q, u, s, v] + gamma2[q, u, v, s])
            + g[p, r, u, v] * gamma2[q, s, u, v]
            for v in relevant_orbs
            for u in relevant_orbs
        )

        return delta * (f[p, s] + f[s, p]) - 2 * h[p, s] * gamma1[q, r] + 2 * inner_sum

    def _compute_orbital_gradients(self):
        """
        Computes orbital gradients.
        """
        self._orbital_gradients = [
            self._get_orbital_gradient(i) for i in range(len(self._initial_circuits))
        ]

        self._orbital_gradient_avg = sum(
            w * g for w, g in zip(self.weights, self._orbital_gradients)
        )

    def _get_orbital_gradient(self, state_idx: int) -> np.array:
        grad = np.zeros((self._n_mo_optim * (self._n_mo_optim - 1) // 2))
        for q in range(self._n_mo_optim - 1):
            for p in range(q + 1, self._n_mo_optim):
                grad[self._get_orbital_idx(p, q)] = 2 * (
                        self._fock_mats[state_idx][p, q] - self._fock_mats[state_idx][q, p]
                )

        return grad

    def _compute_fock_mats(self):
        self._fock_mats = [
            self._get_fock_from_idx(i) for i in range(len(self._initial_circuits))
        ]
        self._compute_st_avg_fock()

    def _get_fock_from_idx(self, state_idx: int) -> np.array:
        return self._get_fock(
            self._one_body_reduced_density_mats[state_idx],
            self._two_body_reduced_density_mats[state_idx],
        )

    def _get_fock(self, one_body_rdm: np.array, two_body_rdm: np.array) -> np.array:
        # Number of molecular orbitals
        n_mo = self.problem.n_molecular_orbitals

        # Two-body electronic integrals
        g = self._problem.full_ham_two_body_integrals_mo

        # One-body reduced-density matrix
        gamma1 = one_body_rdm

        # Two-body reduced-density matrix
        gamma2 = two_body_rdm

        # Frozen-space Fock operator
        frozen_f = self._get_frozen_fock_op()

        # Active-space Fock operator
        active_f = self._get_active_fock_op(one_body_rdm)

        mat = np.zeros((n_mo, n_mo))

        for q in range(n_mo):
            for i in self._problem.frozen_orbitals_indices:
                mat[i, q] += 2 * (frozen_f[q, i] + active_f[q, i])

            for v in self._problem.active_orbitals:
                mat[v, q] += sum(
                    frozen_f[q, w] * gamma1[v, w] for w in self._problem.active_orbitals
                ) + sum(
                    gamma2[v, w, x, y] * g[q, y, x, w]
                    for w in self._problem.active_orbitals
                    for x in self._problem.active_orbitals
                    for y in self._problem.active_orbitals
                )

        return mat

    def _compute_st_avg_fock(
            self,
    ) -> np.array:
        # Number of molecular orbitals
        n_mo = self._problem.n_molecular_orbitals

        # Two-body electronic integrals
        g = self._problem.full_ham_two_body_integrals_mo

        # One-body reduced-density matrix
        gamma1 = self._one_body_reduced_density_mat_avg

        # Two-body reduced-density matrix
        gamma2 = self._two_body_reduced_density_mat_avg

        # Frozen-space Fock operator
        frozen_f = self._get_frozen_fock_op()

        # Active-space Fock operator
        active_f = self._get_active_st_avg_fock_op()

        mat = np.zeros((n_mo, n_mo))

        for q in range(n_mo):
            for i in self._problem.frozen_orbitals_indices:
                mat[i, q] += 2 * (frozen_f[q, i] + active_f[q, i])

            for v in self._problem.active_orbitals:
                mat[v, q] += sum(
                    frozen_f[q, w] * gamma1[v, w] for w in self._problem.active_orbitals
                ) + sum(
                    gamma2[v, w, x, y] * g[q, y, x, w]
                    for w in self._problem.active_orbitals
                    for x in self._problem.active_orbitals
                    for y in self._problem.active_orbitals
                )

        self._fock_mat_avg = mat

    def _get_frozen_fock_op(self) -> np.array:
        # Number of all molecular orbitals
        n_mo = self._problem.n_molecular_orbitals

        # One-body electronic integrals
        h = self._problem.full_ham_one_body_integrals_mo

        # Two-body electronic integrals
        g = self._problem.full_ham_two_body_integrals_mo

        mat = np.zeros((n_mo, n_mo))

        for p in range(n_mo):
            for q in range(n_mo):
                mat[p, q] += h[p, q] + sum(
                    2 * g[p, i, i, q] - g[p, q, i, i]
                    for i in self._problem.frozen_orbitals_indices
                )

        return mat

    def _get_active_st_avg_fock_op(self) -> np.array:
        # Number of all molecular orbitals
        n_mo = self._problem.n_molecular_orbitals

        # Two-body electronic integrals
        g = self._problem.full_ham_two_body_integrals_mo

        # One-body reduced-density matrix
        gamma = self._one_body_reduced_density_mat_avg

        mat = np.zeros((n_mo, n_mo))

        for p in range(n_mo):
            for q in range(n_mo):
                mat[p, q] += sum(
                    gamma[w, x] * (g[p, x, w, q] - 0.5 * g[p, q, w, x])
                    for w in self._problem.active_orbitals
                    for x in self._problem.active_orbitals
                )

        return mat

    def _get_active_fock_op_from_idx(self, state_idx: int) -> np.array:
        return self._get_active_fock_op(self._one_body_reduced_density_mats[state_idx])

    def _get_active_fock_op(self, one_body_rdm: np.array) -> np.array:
        # Number of all molecular orbitals
        n_mo = self._problem.n_molecular_orbitals

        # Two-body electronic integrals
        g = self._problem.full_ham_two_body_integrals_mo

        # One-body reduced-density matrix
        gamma = one_body_rdm

        mat = np.zeros((n_mo, n_mo))

        for p in range(n_mo):
            for q in range(n_mo):
                mat[p, q] += sum(
                    gamma[w, x] * (g[p, x, w, q] - 0.5 * g[p, q, w, x])
                    for w in self._problem.active_orbitals
                    for x in self._problem.active_orbitals
                )

        return mat

    def _get_rdm1_from_idx(
            self, state_idx: int, circuits: list[QuantumCircuit] | OrthogonalCircuitSet
    ) -> np.array:
        return self._get_rdm1(circuits[state_idx])

    def _get_rdm1(self, circuit: QuantumCircuit) -> np.array:
        """
        Obtain one-body reduced density matrix.

        :param circuit:
        :return:
        """

        # Number of molecular orbitals
        n_mo = self.problem.n_molecular_orbitals

        if self._one_body_exc_op_evaluators is None:
            if self._problem.one_body_exc_op_active is None:
                self._problem.create_1_body_exc_op_active()
            self._construct_1_body_ferm_op_evaluators()

        # Evaluation functions for separate terms of the Hamiltonian
        eval_funcs = self._get_eval_funcs_one_body_terms(circuit)

        # Number of active molecular orbitals
        n_acmo = self._problem.n_orbitals_active

        # Assembling of reduced-density matrix
        rdm = np.zeros((n_mo, n_mo))

        for i in self._problem.frozen_orbitals_indices:
            for j in self._problem.frozen_orbitals_indices:
                rdm[i, j] = 2 * (i == j)

        idx_shift = self._problem.active_orbitals[0]
        for p in range(n_acmo):
            for q in range(n_acmo):
                rdm[p + idx_shift, q + idx_shift] += eval_funcs[p][q]([])

        return rdm

    def _get_rdm2_from_idx(
            self,
            state_idx: int,
            one_body_rdm: np.array,
            circuits: list[QuantumCircuit] | OrthogonalCircuitSet,
    ) -> np.array:
        return self._get_rdm2(circuits[state_idx], one_body_rdm)

    def _get_rdm2(self, circuit: QuantumCircuit, one_body_rdm: np.array) -> np.array:
        """
        Obtain two-body reduced density matrix.

        :param circuit:
        :param one_body_rdm:
        :return:
        """

        # Number of molecular orbitals
        n_mo = self.problem.n_molecular_orbitals

        if self._two_body_exc_op_evaluators is None:
            if self._problem.two_body_exc_op_active is None:
                self._problem.create_2_body_exc_op_active()
            self._construct_2_body_ferm_op_evaluators()

        # Evaluation functions for one-body excitation operator \widehat{E}
        eval_funcs = self._get_eval_funcs_two_body_terms(circuit)

        # Number of active molecular orbitals
        n_acmo = self._problem.n_orbitals_active

        # One-body reduced density matrix
        rdm1 = one_body_rdm

        rdm = np.zeros((n_mo, n_mo, n_mo, n_mo))

        for i in self._problem.frozen_orbitals_indices:
            for j in self._problem.frozen_orbitals_indices:
                for k in self._problem.frozen_orbitals_indices:
                    for l in self._problem.frozen_orbitals_indices:
                        rdm[i, j, k, l] = 4 * (i == j) * (k == l) - 2 * (i == l) * (
                                j == k
                        )

                for w in self._problem.active_orbitals:
                    for x in self._problem.active_orbitals:
                        rdm[i, j, w, x] = rdm[w, x, i, j] = 2 * rdm1[w, x] * (i == j)
                        rdm[i, w, x, j] = rdm[x, j, i, w] = -rdm1[w, x] * (i == j)

        # Assembling of reduced-density matrix
        idx_shift = self._problem.active_orbitals[0]
        for p in range(n_acmo):
            for q in range(n_acmo):
                for r in range(n_acmo):
                    for s in range(n_acmo):
                        rdm[
                            p + idx_shift, q + idx_shift, r + idx_shift, s + idx_shift
                        ] += eval_funcs[p][q][r][s]([])

        return rdm

    def _get_eval_funcs_one_body_terms(self, state_circuit: QuantumCircuit) -> list:
        return [
            [e.get_evaluation_func(state_circuit) for e in lst]
            for lst in self._one_body_exc_op_evaluators
        ]

    def _get_eval_funcs_two_body_terms(self, state_circuit: QuantumCircuit) -> list:
        return [
            [
                [[e.get_evaluation_func(state_circuit) for e in lst3] for lst3 in lst2]
                for lst2 in lst
            ]
            for lst in self._two_body_exc_op_evaluators
        ]

    def _construct_1_body_ferm_op_evaluators(self):
        self._one_body_exc_op_evaluators = [
            [
                HermitianOperatorEvaluator(
                    self._problem.fermionic_mapper.map(op), self._estimator
                )
                for op in lst
            ]
            for lst in self._problem.one_body_exc_op_active
        ]
        # self._one_body_exc_op_evaluators = [[HermitianOperatorEvaluator(
        # self._problem.fermionic_mapper.map(op),
        #                                                                 self._estimator)
        #                                      for op in lst]
        #                                     for lst in
        #                                     self._problem.one_body_exc_op_active]

    def _construct_2_body_ferm_op_evaluators(self):
        self._two_body_exc_op_evaluators = [
            [
                [
                    [
                        HermitianOperatorEvaluator(
                            self._problem.fermionic_mapper.map(op), self._estimator
                        )
                        for op in lst3
                    ]
                    for lst3 in lst2
                ]
                for lst2 in lst1
            ]
            for lst1 in self._problem.two_body_exc_op_active
        ]

        # self._two_body_exc_op_evaluators = [
        #     [[[HermitianOperatorEvaluator(
        #     self._problem.fermionic_mapper.map(op),
        #                                   self._estimator)
        #        for op in lst3]
        #       for lst3 in lst2]
        #      for lst2 in lst1]
        #     for lst1 in self._problem.two_body_exc_op_active]

    def _construct_gradient_evaluators(
            self,
            operator_evaluator: HermitianOperatorEvaluator,
            parametrized_grad_circuits: list[QuantumCircuit] | OrthogonalCircuitSet,
    ):
        self._gradient_evaluators = [
            GradientEvaluator(
                circ,
                operator_evaluator,
                circ.parameters,
                grad_method=GradMethod.FINITE_DIFF,
                hess_method=GradMethod.FINITE_DIFF,
            )
            for circ in parametrized_grad_circuits
        ]

    def _construct_ham_nuc_deriv_grad_evaluators(self, atom_idx, state_idx):
        ham_deriv_ops = self._problem.get_qubit_hamiltonian_nuclear_derivative_op(
            atom_idx
        )
        self._ham_nuc_deriv_grad_evaluators[state_idx][atom_idx] = [
            GradientEvaluator(
                self._parametrized_grad_circuits[state_idx],
                HermitianOperatorEvaluator(ham_deriv_ops[i], self._estimator),
                self._ansatz.parameters,
                grad_method=GradMethod.FINITE_DIFF,
                hess_method=GradMethod.FINITE_DIFF,
            )
            for i in range(3)
        ]

    def _get_eng_funcs(self, circuits: Union[OrthogonalCircuitSet, list, tuple]):
        # Create circuits (ansatz + initial states) -> |PsiA(theta)>,
        # |PsiB(theta)>, ...
        # and obtain energy functions providing <PsiA|H|PsiA>,
        # <PsiB|H|PsiB>, ...
        #
        # Works only with ACTIVE Hamiltonian to minimize runtime!!!
        eng_funcs = None
        try:
            eng_funcs = [
                self._active_hamiltonian_evaluator.get_evaluation_func(c)
                for c in circuits
            ]

        except AttributeError as e:
            print(
                "Hint: Pay attention to variable 'circuits' - It needs to "
                "be either OrthogonalCircuitSet or list "
                "of QuantumCircuit, not a single QuantumCircuit itself!",
                file=sys.stderr,
            )
            raise e

        return eng_funcs

    def _cost_function_state_averaged_energy(
            self,
            params: Union[list[float], np.array],
            eng_funcs: Union[tuple[Callable], list[Callable]],
            s_squared_funcs: Union[tuple[Callable], list[Callable]],
            s_squared_cost_coeff: float,
    ) -> float:
        """
        Attributes:

        params (list): values of the ansatz parameters (to be fitted)
        eng_funcs (list): list of energy functions generated by qiskit:
        get_energy_evaluation
        weights (list): values of the weights of the state-averaged ensemble.

        Returns: State-averaged energy
        """
        return sum(
            (f(params) + s_squared_cost_coeff * s_squared_funcs[i](params))
            * self._weights[i]
            for i, f in enumerate(eng_funcs)
        ).real

    def _weights_attribution(self, choice) -> list[float]:
        """
        Attributes:

        n_states: number of states
        choice: defines the values of the weights (equi-weighted,
        or by decreasing order)

        Returns: list of weights
        """

        n_states = self._n_states
        weights = {
            WeightAttribution.EQUIVALENT: [1.0 / n_states] * n_states,
            WeightAttribution.DECREASING: [
                (1.0 + i) / (n_states * (n_states + 1.0) / 2)
                for i in reversed(range(n_states))
            ],
        }

        return weights[choice]

    def _get_hadamard_test_circ(self, circ1: QuantumCircuit, circ2: QuantumCircuit) -> QuantumCircuit:
        # TODO is it necessary to work also with imaginary part?

        # Create Unitaries U1^dagger and U2
        num_qubits = self.problem.n_qubits
        u_1_daggger = circ1.to_gate().inverse()
        u_2 = circ2.to_gate()

        # Create controlled Unitary Ut
        u_circ = QuantumCircuit(num_qubits)
        u_circ.append(u_2, [i for i in range(num_qubits)])
        u_circ.append(u_1_daggger, [i for i in range(num_qubits)])
        u_control = u_circ.to_gate().control(1)

        # Create circuit for the real part
        hadamard_test_circuit_real = QuantumCircuit(num_qubits + 1, 1)
        hadamard_test_circuit_real.h(0)
        hadamard_test_circuit_real.append(u_control, [i for i in range(num_qubits + 1)])
        hadamard_test_circuit_real.h(0)
        hadamard_test_circuit_real.measure(0, 0)

        return hadamard_test_circuit_real
