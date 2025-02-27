"""
Tests for diabatization settings.
"""
import logging
from pathlib import Path
import numpy as np
from qiskit_algorithms.optimizers import SciPyOptimizer
import saoovqe
import pytest
from qiskit.primitives import Estimator, Sampler
import psi4

# Set the global logger to ERROR level, so that the outputs except errors won't be printed
log = logging.getLogger('SAOOVQE.logger')
log.setLevel(logging.ERROR)


class TestDiabatization:
    """
    Tests for diabatzations of orbitals.
    """

    def test_theta190_phi0(self):
        """
        Testing resulting energies w.r.t. reference values without orbital optimization and with the previous
        wavefunction computed at the point theta 180, phi 0.
        """
        # Method specification
        estimator = Estimator()
        sampler = Sampler()
        n_states = 2
        repetitions = 1

        symbols = ['C', 'N', 'H', 'H', 'H']
        coords = [[-0.000000000, 0.000000000, -0.000000000],
                  [-0.000000000, 0.000000000, 1.412052000],
                  [-0.000000000, -0.944215264, -0.525349226],
                  [-0.000000000, 0.944215264, -0.525349226],
                  [-0.176643782, 0.000000000, 2.413848671]]

        # Molecule specification

        n_orbs_active = 2
        n_elec_active = 2
        charge = 0
        multiplicity = 1
        basis = 'sto-3g'

        load_wfn = psi4.core.Wavefunction.from_file(f'{Path(__file__).resolve().parent.parent}/'
                                                    f'tests/wfn_phi0_theta_180_sto3g')

        # Problem creation
        problem = saoovqe.ProblemSet.with_dia_orbs_from_prev_wfn(symbols, coords, charge, multiplicity, n_elec_active,
                                                                 n_orbs_active, load_wfn, basis)

        # Step 1: Initialization - states |phiA>, |phiB>
        initial_circuits = saoovqe.OrthogonalCircuitSet.from_problem_set(n_states, problem)

        # Define the ansatz circuit:
        # Operator Û(theta)
        ansatz = saoovqe.Ansatz.from_problem_set(saoovqe.AnsatzType.GUCCSD,
                                                 problem,
                                                 repetitions,
                                                 qubit_mapper=problem.fermionic_mapper)

        # Perform SA-VQE procedure
        saoovqe_solver = saoovqe.SAOOVQE(estimator,
                                         initial_circuits,
                                         ansatz,
                                         problem,
                                         orbital_optimization_settings={})

        energies = saoovqe_solver.get_energy(SciPyOptimizer('SLSQP', options={'maxiter': 500, 'ftol': 1e-8}))

        assert np.allclose(np.array([-92.69532984620506, -92.64558680739152]), energies)

        # Store the solver into Pytest namespace
        pytest.solver = saoovqe_solver

    @pytest.mark.dependency(depends=['test_theta190_phi0'])
    def test_eval_eng_gradient_theta190_phi0(self):
        """
        Testing gradients for all atoms and the first two doublet states w.r.t. reference values without
        orbital-optimization and with the previous wavefunction computed at the point theta 180, phi 0.
        """

        grad_results = np.array([[[0.01150584785724335, -1.311599689259345e-07, -0.47740794751829313],
                                  [0.01126357582762757, 3.2526437470153823e-07, 0.44663602910876976],
                                  [-0.006466890057894573, 0.00704541478957155, 0.012428722860131459],
                                  [-0.006466039864754627, -0.007045401747328432, 0.012428762082927328],
                                  [-0.009836493762273342, -2.0719664279549483e-07, 0.005914433466547057]],

                                 [[0.026305348771842953, 1.3007404240234663e-07, -0.13641358401233047],
                                  [-0.05988061577591204, -3.2209753910807767e-07, 0.13522519626871796],
                                  [-0.0002666662219992505, 0.0006257089824901513, -0.0048939410581390315],
                                  [-0.00026750432257994643, -0.0006257219092520401, -0.004893979947161909],
                                  [0.034109437548886984, 2.0500066629968857e-07, 0.010976308749072534]]])

        for state_idx in range(2):
            for atom_idx in range(5):
                assert np.allclose(pytest.solver.eval_eng_gradient(state_idx, atom_idx),
                                   grad_results[state_idx][atom_idx],
                                   atol=1e-2)

    @pytest.mark.dependency(depends=['test_eval_eng_gradient_theta190_phi0'])
    def test_eval_nac_theta190_phi0(self):
        """
        Testing computation of non-adiabatic couplings without orbital-optimization and after get_energy() and
        eval_eng_gradient() manually called and with the previous wavefunction computed at the point theta 180, phi 0.
        """

        nac_results = np.array(
            [[3.391159960099604e-06, -0.32131769741088406, -4.7828618301924956e-05],
             [1.535757382529377e-06, 0.6479933642713491, 1.9443881365387564e-05],
             [-0.6074889097232339, 0.017012297302320793, -0.0504531067223181],
             [0.6074863865561233, 0.017003548653003988, 0.05046907938413269],
             [-2.25519871628663e-06, -0.3994716165968752, 1.1810260542595427e-05]])

        for atom_idx in range(5):
            pytest.solver.eval_nac(atom_idx)
            assert np.allclose(pytest.solver.total_nacs[atom_idx], -nac_results[atom_idx], atol=1e-2)
