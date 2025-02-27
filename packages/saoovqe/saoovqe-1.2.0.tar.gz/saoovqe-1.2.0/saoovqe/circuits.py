"""Module for fast manipulation with often-used circuits.

Module comprising classes implementing an orthogonal set of circuits
representing parts of initial to-be-optimized state vectors.
"""

from abc import ABC, abstractmethod
from typing import Optional, Callable, Union

import numpy as np
import qiskit_nature
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.primitives import BaseEstimatorV1, BaseEstimatorV2, BackendEstimatorV2, BackendEstimator
from qiskit.providers import BackendV1, BackendV2
from qiskit.quantum_info import Statevector
from qiskit_ibm_runtime import EstimatorV2
from qiskit_nature.second_q.circuit.library import HartreeFock
from qiskit_nature.second_q.mappers import QubitMapper

from .logger_config import log
from .problem import ProblemSet

###########
# Settings
###########
qiskit_nature.settings.dict_aux_operators = True


# TODO does this class belong into circuits.py?
class OperatorEvaluatorBase(ABC):
    """
    Base class for evaluator of operators' expectation values.
    """

    def __init__(self, operator, estimator: Union[BackendEstimator, BackendEstimatorV2, EstimatorV2]) -> None:
        """
        Constructor

        :param operator: Operator whose expectation values are to be evaluated.
        :param estimator: BaseEstimator instance providing measurement
        implementation.
        """
        self._operator = operator
        self._estimator = estimator

    @abstractmethod
    def get_evaluation_func(self, circuit: QuantumCircuit) -> Callable:
        """
        Returns an evaluation function, which returns expectation values for
        provided parameters.

        :param circuit: Quantum Circuit
        :return: Function returning expectation values
        """


# TODO does this class belong into circuits.py?
class HermitianOperatorEvaluator(OperatorEvaluatorBase):
    """
    Expectation value evaluator for Hermitian operators.
    """

    def get_evaluation_func(self, circuit: QuantumCircuit) -> Callable:
        """
        Obtain evaluation function (i.e. a function returning expectation
        values when provided parameters).

        :param circuit:  Quantum circuit representing a parametrized state
            vector w.r.t. which the expectation values are computed.

        :return: Evaluation function
        """

        if isinstance(self._estimator, EstimatorV2):
            circuit = transpile(circuit, backend=self._estimator.session._backend)

        def evaluation_func(circ_params: list[float] | np.ndarray) -> float | complex:
            """
            Function returning expectation values for the chosen operator
            and a state vector circuit w.r.t. provided
            circuit parameters.

            :param circ_params: Parameters for the circuit (representing a
                state vector)

            :return: Expectation value
            """
            param_binding = None
            if isinstance(circ_params, dict):
                param_binding = circ_params
            else:
                param_binding = {
                    p: circ_params[i] for i, p in enumerate(circuit.parameters)
                }

            # TODO Simplify, when migrating to Qiskit v1.2
            # t=self._estimator.run([(circuit, self._operator, param_binding)])
            # # print('asdf')
            # # print(t)
            # # print(t.result())
            # # print(t.result()[0])
            # # print(t.result()[0].data)
            # # print(t.result()[0].data.evs)
            # # exit(-1)
            return (
                self._estimator.run(circuit.assign_parameters(param_binding), self._operator).result().values[0]
                if isinstance(self._estimator, BaseEstimatorV1)
                else self._estimator.run([(circuit, self._operator, param_binding)])

            )

        return evaluation_func

    @property
    def operator(self):
        """
        Operator whose expectation values are being evaluated.
        """
        return self._operator

    @property
    def estimator(self):
        """
        Estimator providing implementation of a measurement.
        """
        return self._estimator


# class FastOperatorEvaluator:
#     """
#     Simple statevector evaluator of operators' expectation values.
#     """
#
#     def __init__(self, operator, mapper) -> None:
#         self._mapper = mapper
#         self._qubit_operator = operator
#         self._mat_operator = self._qubit_operator.to_matrix()
#
#     def get_evaluation_func(self, circuit: QuantumCircuit) -> Callable:
#         """
#         Obtain evaluation function (i.e. a function returning expectation
#         values when provided parameters).
#
#         :param circuit:  Quantum circuit representing a parametrized state
#         vector w.r.t. which the expectation values
#                          are computed.
#
#         :return: Evaluation function
#         """
#
#         def evaluation_func(circ_params: list[float] | np.ndarray) -> float:
#             """
#             Function returning expectation values for the chosen operator
#             and a state vector circuit w.r.t. provided
#             circuit parameters.
#
#             :param circ_params: Parameters for the circuit (representing a
#             state vector)
#
#             :return: Expectation value
#             """
#             sv = Statevector(circuit.assign_parameters(circ_params)).data
#
#             return (sv.conj() @ self._mat_operator @ sv).real
#
#         return evaluation_func


class OrthogonalCircuitSet:
    """
    Implementation of a circuit set representing parts of orthogonal state
    vectors.
    """

    # TODO make more general, not only for initial circuits
    def __init__(
        self,
        n_states: int,
        n_spatial_orbs: int,
        n_particles: tuple[int, int],
        qubit_mapper: Optional[QubitMapper] = None,
    ):
        """
        Creates an instance of OrthogonalCircuitSet.

        :param n_states: Number of states/
        :param n_spatial_orbs: Number of spatial molecular orbitals.
        :param n_particles: Number of particles in the system in the format
        (no. alpha particles, no. beta particles).
        :param qubit_mapper: Qubit mapper encoding operators to quantum
        circuits.
        """
        self._n_states = n_states
        self._n_spatial_orbs = n_spatial_orbs
        self._n_particles = n_particles
        self._qubit_mapper = qubit_mapper

        if n_states > 3:
            raise ValueError(
                "No more than three states in the ensemble are supported for now"
            )

        # Ground state circuit |HF>
        #   Paper notation: |PhiA>
        self._circuits = [self._ground_state_circuit()]

        self._n_qubits = self._circuits[0].num_qubits

        if n_states > 1:
            self._circuits.append(self._singly_excited_singlet_circuit())

        if n_states > 2:
            self._circuits.append(self._doubly_excited_singlet_circuit())

        log.info("Circuits representing an orthogonal basis were created.")

    @classmethod
    def from_problem_set(cls, n_states: int, problem: ProblemSet):
        """
        Alternative constructor for making instance of
        :class:`OrthogonalCircuitSet` from :class:`problem.ProblemSet`
        instance.

        :param n_states: Number of quantum states.
        :param problem: :class:`problem.ProblemSet` instance

        :return Instance of :class:`OrthogonalCircuitSet` created w.r.t.
        "problem" parameter
        """
        return cls(
            n_states,
            problem.as_problem.num_spatial_orbitals,
            problem.as_problem.num_particles,
            qubit_mapper=problem.fermionic_mapper,
        )

    def __len__(self):
        return len(self._circuits)

    def __getitem__(self, idx):
        return self._circuits[idx]

    @property
    def n_states(self):
        """
        Number of quantum states
        """
        return self._n_states

    @property
    def n_qubits(self):
        """
        Number of qubits
        """
        return self._n_qubits

    @property
    def n_particles(self):
        """
        Number of particles
        """
        return self._n_particles

    @property
    def circuits(self):
        """
        Constructed quantum circuits
        """
        return self._circuits

    @property
    def qubit_converter(self):
        """
        Qubit mapper for encoding of operators to quantum circuits
        """
        return self._qubit_mapper

    def get_new_rotation_circuit(self):
        r"""
        Obtain :math:`|\psi_0\rangle = \cos(\varphi)|\psi_A\rangle + \sin(
        \varphi)|\psi_B\rangle`
        by applying the rotating circuit to :math:`|0000\rangle`

        This DOES NOT require any knowledge of initial
        :math:`|\psi_A\rangle` or :math:`|\psi_B\rangle` vectors
        """

        circuit = QuantumCircuit(self._n_qubits)
        self.add_resolution_rotation_circuit(circuit)
        return circuit

    def _ground_state_circuit(self):
        # First state is the HF state. Note that the orbitals are sorted
        # with first spin alpha and then spin beta.
        #   Ex. 4 qubits: |0101> (in Qiskit order)
        circuit = HartreeFock(
            num_spatial_orbitals=self._n_spatial_orbs,
            num_particles=self._n_particles,
            qubit_mapper=self._qubit_mapper,
        )

        return circuit

    def transpile(self, backend: Union[BackendV1, BackendV2]):
        """
        Transpiles the circuits in-place w.r.t. the provided backend.

        :param backend: The backend w.r.t. whose gate set the circuits are going to be transpiled.
        """
        self._circuits = [transpile(circ, backend=backend) for circ in self._circuits]

    def add_resolution_rotation_circuit(
        self, circuit: QuantumCircuit, rotation_angle: Optional[float] = None
    ):
        r"""
        Creates the singly-excited singlet excitation (superposition of one
        spin-up and one spin-down excitation)
        see Fig. 1 in Ref. https://doi.org/10.1021/acs.jctc.1c00995

        If applied to :math:`|0000\rangle` with :math:`\varphi=0`,
        transforms the state to
        :math:`|0101\rangle = |\text{HF}\rangle`.
        """
        (n_alpha, n_beta) = self.n_particles

        # set all N-2 electrons in the lowest alpha- and beta-occupied
        # spin-orbitals
        for i in range(n_alpha - 1):
            circuit.x(i)
        for i in range(n_beta - 1):
            circuit.x(self._n_qubits // 2 + i)

        # Adjust the rotation angle logic
        if rotation_angle is None:
            circuit.ry(2 * Parameter("RotAngle"), n_alpha - 1)
        else:
            circuit.ry(2 * rotation_angle, n_alpha - 1)

        # Adjust the rest of the operations
        circuit.x(self.n_qubits // 2 + n_beta - 1)
        circuit.ch(n_alpha - 1, self.n_qubits // 2 + n_beta)
        circuit.cx(self.n_qubits // 2 + n_beta, self.n_qubits // 2 + n_beta - 1)
        circuit.cx(self.n_qubits // 2 + n_beta, n_alpha - 1)
        circuit.cx(n_alpha - 1, n_alpha)
        circuit.x(n_alpha - 1)

    def _singly_excited_singlet_circuit(self):
        circuit = QuantumCircuit(self._n_qubits)
        self.add_resolution_rotation_circuit(circuit, rotation_angle=np.pi / 2)

        return circuit

    def _doubly_excited_singlet_circuit(self):
        circuit = QuantumCircuit(self._n_qubits)
        n_alpha, n_beta = self._n_particles

        # TODO check & fix, if necessary!

        # Creates the doubly-excited singlet excitation (spin-up and
        # spin-down excitations)
        circuit.x(n_alpha + 1)
        circuit.x(self._n_qubits // 2 + n_beta)

        return circuit
