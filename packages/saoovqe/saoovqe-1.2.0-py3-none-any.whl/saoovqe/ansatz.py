"""API to enable fast creation of ansatzes.

Module containing the class representing an ansatz for SA-OO-VQE method, where all the inner
coefficients are either 1 or -1.
"""

from enum import Enum, auto
from typing import Tuple
from qiskit.circuit import ParameterExpression
from qiskit.circuit.library import TwoLocal, NLocal
from qiskit_nature.second_q.circuit.library import UCC
from qiskit_nature.second_q.mappers.fermionic_mapper import FermionicMapper
from sympy import simplify

from .vqe_optimization import ProblemSet
from .logger_config import log


class NoValueEnum(Enum):
    """
    Utility class for printing settings of AnsatzType elements.
    """

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}>"


class AnsatzType(NoValueEnum):
    """
    Enumerator representing the set of available ansatz structures.
    """

    TWO_LOCAL = auto()
    UCCS = auto()
    UCCD = auto()
    GUCCD = auto()
    UCCSD = auto()
    GUCCSD = auto()


class Ansatz(NLocal):
    """
    Ansatz prepared for SA-OO-VQE with all inner coefficients set to either
    1 or -1.
    """

    def __new__(
        cls,
        ansatz: AnsatzType,
        n_spatial_orbs: int,
        n_qubits: int,
        n_particle: Tuple[int, int],
        repetitions: int,
        rotation_blocks="ry",
        entanglement_blocks="cx",
        entanglement="linear",
        fermionic_mapper: FermionicMapper = None
    ):
        match ansatz:
            case AnsatzType.TWO_LOCAL:
                circuit = TwoLocal(
                    num_qubits=n_qubits,
                    rotation_blocks=rotation_blocks,
                    entanglement_blocks=entanglement_blocks,
                    entanglement=entanglement,
                    reps=repetitions,
                    skip_unentangled_qubits=False,
                    skip_final_rotation_layer=False,
                    insert_barriers=True,
                    initial_state=None,
                )
            case AnsatzType.UCCS:
                circuit = UCC(
                    num_spatial_orbitals=n_spatial_orbs,
                    qubit_mapper=fermionic_mapper,
                    num_particles=n_particle,
                    excitations="s",
                    alpha_spin=True,
                    beta_spin=True,
                    max_spin_excitation=None,
                    generalized=False,
                    preserve_spin=True,
                    reps=repetitions,
                    initial_state=None,
                )
            case AnsatzType.UCCD:
                circuit = UCC(
                    num_spatial_orbitals=n_spatial_orbs,
                    qubit_mapper=fermionic_mapper,
                    num_particles=n_particle,
                    excitations="d",
                    alpha_spin=True,
                    beta_spin=True,
                    max_spin_excitation=None,
                    generalized=False,
                    preserve_spin=True,
                    reps=repetitions,
                    initial_state=None,
                )
            case AnsatzType.UCCSD:
                circuit = UCC(
                    num_spatial_orbitals=n_spatial_orbs,
                    qubit_mapper=fermionic_mapper,
                    num_particles=n_particle,
                    excitations="sd",
                    alpha_spin=True,
                    beta_spin=True,
                    max_spin_excitation=None,
                    generalized=False,
                    preserve_spin=True,
                    reps=repetitions,
                    initial_state=None,
                )
            case AnsatzType.GUCCD:
                circuit = UCC(
                    num_spatial_orbitals=n_spatial_orbs,
                    qubit_mapper=fermionic_mapper,
                    num_particles=n_particle,
                    excitations="d",
                    alpha_spin=True,
                    beta_spin=True,
                    max_spin_excitation=None,
                    generalized=True,
                    preserve_spin=True,
                    reps=repetitions,
                    initial_state=None,
                )

            case AnsatzType.GUCCSD:
                circuit = UCC(
                    num_spatial_orbitals=n_spatial_orbs,
                    qubit_mapper=fermionic_mapper,
                    num_particles=n_particle,
                    excitations="sd",
                    alpha_spin=True,
                    beta_spin=True,
                    max_spin_excitation=None,
                    generalized=True,
                    preserve_spin=True,
                    reps=repetitions,
                    initial_state=None,
                )
            case _:
                raise ValueError(
                    "Provided ansatz name is not supported! It has to be an "
                    "element of AnsatzType."
                )

        # Let's rewrite all gate coefficients to 1 or -1, because of gradients
        #
        # First of all we'll decompose our ansatz circuit enough to see the
        # separate rotation gates

        circuit = circuit.decompose().decompose().decompose()

        # Now we'll iterate over all gates and choose the parametrized ones
        for i, g in enumerate(circuit):
            params = g.operation.params
            if params:
                # Obtain the SymPy symbol (i.e. independent variable w.r.t.
                # which we compute derivatives)
                symbol = list(params[0]._parameter_symbols.values())[0]

                # Rewrite the SymPy expression to multiplication by 1 or -1
                # (maintaining the sign)
                circuit[i].operation.params[0] = ParameterExpression(
                    params[0]._parameter_symbols,
                    -symbol if simplify(params[0]._symbol_expr).args[0] < 0 else symbol,
                )

        log.info("Ansatz was created.")

        return circuit

    @classmethod
    def from_problem_set(
        cls,
        ansatz: AnsatzType,
        problem: ProblemSet,
        repetitions: int,
        qubit_mapper: FermionicMapper = None,
    ):
        """
        Alternative constructor creating Ansatz instance directly from
        instances of
        :class:`problem.ProblemSet` class.

        :param ansatz: Type of ansatz
        :param problem: :class:`problem.ProblemSetProblemSet` instance
        :param repetitions: Number of block repetitions
        :param qubit_mapper: Mapper used to encode operators to qubits
        :return: An instance of Ansatz class
        """
        return cls(
            ansatz,
            problem.as_problem.num_spatial_orbitals,
            problem.as_operators[0].register_length,
            problem.as_problem.num_particles,
            repetitions,
            fermionic_mapper=qubit_mapper,
        )
