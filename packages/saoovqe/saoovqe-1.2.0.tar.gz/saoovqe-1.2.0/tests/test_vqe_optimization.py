"""
Tests for module vqe_optimization.py.
"""
import logging

import numpy as np
import pytest
from qiskit_algorithms.optimizers import SciPyOptimizer
from qiskit.primitives import Estimator, Sampler
import psi4
from pathlib import Path

import saoovqe

# Set the global logger to ERROR level, so that the outputs except errors
# won't be printed
log = logging.getLogger('SAOOVQE.logger')
log.setLevel(logging.ERROR)


class TestSAOOVQE:
    """
    Tests for class SAOOVQE.
    """

    def test_get_energy(self):
        """
        Testing resulting energies w.r.t. reference values without orbital
        optimization.
        """
        estimator = Estimator()
        n_states = 2
        repetitions = 1
        symbols = ['N', 'C', 'H', 'H', 'H']
        coords = [
            [0.000000000000, 0.000000000000, 0.000000000000],
            [0.000000000000, 0.000000000000, 1.498047000000],
            [0.000000000000, -0.938765985000, 2.004775984000],
            [0.000000000000, 0.938765985000, 2.004775984000],
            [-0.744681452, -0.131307432, -0.634501434]
        ]

        n_orbs_active = 2
        n_elec_active = 2
        charge = 0
        multiplicity = 1
        basis = "sto-3g"
        problem = saoovqe.ProblemSet(symbols, coords, charge, multiplicity,
                                     n_elec_active, n_orbs_active, basis)
        initial_circuits = (
            saoovqe.circuits.OrthogonalCircuitSet.from_problem_set(
                n_states, problem))
        ansatz = saoovqe.ansatz.Ansatz.from_problem_set(
            saoovqe.AnsatzType.GUCCSD, problem,
            repetitions,
            qubit_mapper=problem.fermionic_mapper)
        saoovqe_solver = saoovqe.vqe_optimization.SAOOVQE(estimator,
                                                          initial_circuits,
                                                          ansatz,
                                                          problem)
        energies = saoovqe_solver.get_energy(
            SciPyOptimizer('SLSQP', options={'maxiter': 500, 'ftol': 1e-8}))

        assert np.allclose(energies, [-92.67656932, -92.60856254])
        # Store the solver into Pytest namespace
        pytest.solver = saoovqe_solver

    @pytest.mark.dependency(depends=['test_get_energy'])
    def test_eval_eng_gradient(self):
        """
        Testing gradients for all atoms and the first two doublet states
        w.r.t. reference values without
        orbital-optimization.
        """

        grad_results = np.array([[[-0.11567902, -0.12763289, -0.35587812],
                                  [0.0691202, 0.05507152, 0.383955],
                                  [-0.00855294, 0.02854877, -0.04214174],
                                  [-0.0311405, -0.03379234, -0.02452439],
                                  [0.08625226, 0.07780493, 0.03858924]],
                                 [[-0.12304042, 0.04844685, -0.52807944],
                                  [0.07892739, -0.06963024, 0.48500761],
                                  [0.02885834, 0.02761671, 0.00037695],
                                  [-0.07559798, -0.01748411, -0.01747446],
                                  [0.09085268, 0.01105079, 0.06016933]]])

        for state_idx in range(2):
            for atom_idx in range(5):
                assert np.allclose(
                    pytest.solver.eval_eng_gradient(state_idx, atom_idx),
                    grad_results[state_idx][atom_idx],
                    atol=1e-2)

    @pytest.mark.dependency(depends=['test_eval_eng_gradient'])
    def test_eval_nac(self):
        """
        Testing computation of non-adiabatic couplings without
        orbital-optimization and after get_energy() and
        eval_eng_gradient() manually called.
        """

        nac_ci_results = np.array(
            [[0.5439943498115053, 1.1684088806620296, -0.7477457244563686],
             [0.1712166347299241, -0.08536388690537468, 0.8373463439402303],
             [-1.1346338970763914, 0.10020459027070877, -0.13709419849967547],
             [0.8211696168772007, -0.09051967253491822, -0.20854156734784737],
             [-0.40174670434001025, -1.0927299115141729, 0.2560351462817991]])

        nac_csf_results = np.array(
            [[0.05220481675347806, -0.2729771912002486, 0.0597154908352368],
             [-0.04014856493142028, 0.0396126786135919, 0.05796015322575899],
             [-0.04059385282854357, 0.0014614436897506195,
              0.007672545872993445],
             [0.053939122002934846, 0.0009792714103195328,
              -0.007569510457807933],
             [-0.020111622109421055, 0.09383687955319261,
              0.00534151714497949]])

        for atom_idx in range(5):
            pytest.solver.eval_nac(atom_idx)
            assert np.allclose(-pytest.solver.ci_nacs[atom_idx],
                               nac_ci_results[atom_idx], atol=8e-2)
            assert np.allclose(-pytest.solver.csf_nacs[atom_idx],
                               nac_csf_results[atom_idx], atol=1e-4)

    def test_get_energy_with_oo(self):
        """
        Testing resulting energies w.r.t. reference values with orbital
        optimization in default settings.
        """
        estimator = Estimator()
        n_states = 2
        repetitions = 1
        symbols = ['N', 'C', 'H', 'H', 'H']
        coords = [
            [0.000000000000, 0.000000000000, 0.000000000000],
            [0.000000000000, 0.000000000000, 1.498047000000],
            [0.000000000000, -0.938765985000, 2.004775984000],
            [0.000000000000, 0.938765985000, 2.004775984000],
            [-0.744681452, -0.131307432, -0.634501434]
        ]

        n_orbs_active = 2
        n_elec_active = 2
        charge = 0
        multiplicity = 1
        basis = "sto-3g"
        problem = saoovqe.ProblemSet(symbols, coords, charge, multiplicity,
                                     n_elec_active, n_orbs_active, basis)
        initial_circuits = (
            saoovqe.circuits.OrthogonalCircuitSet.from_problem_set(
                n_states, problem))
        ansatz = saoovqe.ansatz.Ansatz.from_problem_set(
            saoovqe.AnsatzType.GUCCSD, problem,
            repetitions,
            qubit_mapper=problem.fermionic_mapper)
        saoovqe_solver = saoovqe.vqe_optimization.SAOOVQE(estimator,
                                                          initial_circuits,
                                                          ansatz,
                                                          problem,
                                                          orbital_optimization_settings={})
        energies = saoovqe_solver.get_energy(
            SciPyOptimizer('SLSQP', options={'maxiter': 500, 'ftol': 1e-8}))

        assert np.allclose(saoovqe_solver.ansatz_param_values,
                           [0.1137378, 0.11373294, -0.01226826], atol=5e-3)
        assert np.allclose(energies, [-92.68211767, -92.63750356])

        # Store the solver into Pytest namespace
        pytest.solver_oo = saoovqe_solver

    @pytest.mark.dependency(depends=['test_get_energy_with_oo'])
    def test_eval_eng_gradient_with_oo(self):
        """
        Testing gradients for all atoms and the first two doublet states
        w.r.t. reference values with
        orbital-optimization.
        """

        grad_results = np.array([[[-0.22490777960566383, -0.04910219377300623,
                                   -0.20325398514218163],
                                  [0.07463806158292616, 0.017956946069180853,
                                   0.23842835797012024],
                                  [-0.0030110480345959655,
                                   0.024607502956929195,
                                   -0.026045630670931647],
                                  [-0.006390999599623158,
                                   -0.025849042495819072,
                                   -0.02034922532185033],
                                  [0.15967176565669552, 0.032386787242678315,
                                   0.011220483165484928]],
                                 [[-0.040996862234817064, -0.02444420730902424,
                                   -0.5409093395915159],
                                  [0.06480628134958827, 0.001019490170438639,
                                   0.5144404678269967],
                                  [-0.026953209606435186, 0.03144261191891629,
                                   -0.028104361260914847],
                                  [-0.03867878751224716, -0.030202529641271417,
                                   -0.02737458262325833],
                                  [0.04182257800416296, 0.02218463486097362,
                                   0.08194781565041197]]])

        for state_idx in range(2):
            for atom_idx in range(5):
                assert np.allclose(
                    pytest.solver_oo.eval_eng_gradient(state_idx, atom_idx),
                    grad_results[state_idx][atom_idx],
                    atol=5e-3)

    def test_get_energy_with_oo_8orbs(self):
        """
        Testing resulting energies w.r.t. reference values with orbital
        optimization. There are only 8 orbitals
        being optimized here.
        """
        estimator = Estimator()
        n_states = 2
        repetitions = 1
        symbols = ['N', 'C', 'H', 'H', 'H']
        coords = [
            [0.000000000000, 0.000000000000, 0.000000000000],
            [0.000000000000, 0.000000000000, 1.498047000000],
            [0.000000000000, -0.938765985000, 2.004775984000],
            [0.000000000000, 0.938765985000, 2.004775984000],
            [-0.744681452, -0.131307432, -0.634501434]
        ]

        n_orbs_active = 2
        n_elec_active = 2
        charge = 0
        multiplicity = 1
        basis = "sto-3g"
        problem = saoovqe.ProblemSet(symbols, coords, charge, multiplicity,
                                     n_elec_active, n_orbs_active, basis)
        initial_circuits = (
            saoovqe.circuits.OrthogonalCircuitSet.from_problem_set(
                n_states, problem))
        ansatz = saoovqe.ansatz.Ansatz.from_problem_set(
            saoovqe.AnsatzType.GUCCSD, problem,
            repetitions,
            qubit_mapper=problem.fermionic_mapper)
        saoovqe_solver = saoovqe.vqe_optimization.SAOOVQE(estimator,
                                                          initial_circuits,
                                                          ansatz,
                                                          problem,
                                                          orbital_optimization_settings={
                                                              'n_mo_optim': 8})
        energies = saoovqe_solver.get_energy(
            SciPyOptimizer('SLSQP', options={'maxiter': 500, 'ftol': 1e-8}))

        assert np.allclose(saoovqe_solver.ansatz_param_values,
                           [0.22275567, 0.22276517, -0.01417001], atol=5e-3)
        assert np.allclose(energies, [-92.67111753491074, -92.61717212127579],
                           atol=5e-3)

        # Store the solver into Pytest namespace
        pytest.solver_oo_8 = saoovqe_solver

    @pytest.mark.dependency(depends=['test_get_energy_with_oo_8orbs'])
    def test_eval_eng_gradient_with_oo_8orbs(self):
        """
        Testing gradients for all atoms and the first two doublet states
        w.r.t. reference values with
        orbital-optimization focused only on 8 orbitals.
        """

        grad_results = np.array(
            [[[-0.11603003395745293, -0.1351739135414719, -0.3930387975782544],
              [0.07645069338860756, 0.0631752769835117, 0.4189281842970389],
              [-0.011470842982352491, 0.030554869645770883,
               -0.043515724344877584],
              [-0.034424426486394086, -0.03717679330814408,
               -0.02689905789849448],
              [0.08547461003818918, 0.07862056022100006, 0.0445253955259365]],
             [[-0.22859756666112496, 0.14304818155833718,
               -0.37074110509529434],
              [0.0816588220005738, -0.07293151923281435, 0.33647448904585203],
              [-0.04025171994217064, 0.008349305260783169,
               -0.011552900258461998],
              [0.020404804999027446, -0.004666067628659394,
               -0.031391484276190054],
              [0.16678565960307729, -0.0737998999583281,
               0.07721100058504252]]])

        for state_idx in range(2):
            for atom_idx in range(5):
                assert np.allclose(
                    pytest.solver_oo_8.eval_eng_gradient(state_idx, atom_idx),
                    grad_results[state_idx][atom_idx],
                    atol=5e-3)

    @pytest.mark.dependency(depends=['test_eval_eng_gradient_with_oo_8orbs'])
    def test_eval_nac_with_oo_8orbs(self):
        """
        Testing computation of non-adiabatic couplings with 8
        orbital-optimized molecular orbitals and after
        get_energy() and eval_eng_gradient() manually called.
        """

        nac_ci_results = np.array(
            [[1.536586211250138, 1.703142272151712, -1.99315773150757],
             [-0.04594502116336462, -0.9573431850894599, 2.0066837595666955],
             [-0.236489765711876, 0.2557054798949113, 0.022216043086264785],
             [-0.24169115142149247, -0.1687710053638721, -0.20245479934440358],
             [-1.012460272951729, -0.8327335615894573, 0.16671272823142574]])

        nac_csf_results = np.array(
            [[0.04167769169175575, -0.2855941457208787, 0.04984832077561236],
             [-0.02242484271301797, 0.04654190195250341, 0.042843143861842584],
             [-0.038934294245578135, 0.001479171898964883,
              0.006540470036495448],
             [0.0473998719016068, 0.0009998411378498617,
              -0.006655700873901668],
             [-0.018467116598825807, 0.09755481439303845,
              -0.0008500653272610849]])

        for atom_idx in range(5):
            pytest.solver_oo_8.eval_nac(atom_idx)
            assert np.allclose(-pytest.solver_oo_8.ci_nacs[atom_idx],
                               nac_ci_results[atom_idx], atol=8e-2)
            assert np.allclose(-pytest.solver_oo_8.csf_nacs[atom_idx],
                               nac_csf_results[atom_idx], atol=3e-4)

    @pytest.mark.dependency(depends=['test_eval_eng_gradient_with_oo'])
    def test_eval_nac_with_oo(self):
        """
        Testing computation of non-adiabatic couplings with all molecular
        orbitals optimized and after get_energy() and
        eval_eng_gradient() manually called.
        """

        nac_ci_results = np.array(
            [[0.5166240524959994, -2.138117103724991, -1.250691189076822],
             [0.12040592412388783, 1.06659704691226, 1.2860855648409277],
             [0.011494840741303405, -0.018313907122214604,
              -0.22606499704367056],
             [-0.29463087507778163, -0.08712637990274806, 0.10850835739917179],
             [-0.3538939422932946, 1.176960343835802, 0.08216226385829299]])

        nac_csf_results = np.array(
            [[0.0413405658299385, -0.2132409012467664, -7.866614950090548e-05],
             [0.006733521773318629, 0.031163814933883403,
              0.0009491392756130882],
             [-0.04598211485902906, 0.0014460525347565845,
              0.004100018255751621],
             [0.040431400381969136, 0.0013919817866739556,
              -0.00407964175337271],
             [-0.007971231189508635, 0.07185327650614094,
              -0.004050057420288945]])

        for atom_idx in range(5):
            pytest.solver_oo.eval_nac(atom_idx)
            assert np.allclose(-pytest.solver_oo.ci_nacs[atom_idx],
                               nac_ci_results[atom_idx], atol=8e-2)
            assert np.allclose(-pytest.solver_oo.csf_nacs[atom_idx],
                               nac_csf_results[atom_idx], atol=1e-4)

    def test_get_energy_with_oo_4_3(self):
        """
        Testing resulting energies w.r.t. reference values with orbital
        optimization in default settings. In this case
        the problem is larger, with active space containing 3 molecular
        orbitals and 4 electrons.
        """
        estimator = Estimator()
        n_states = 2
        repetitions = 1
        symbols = ['N', 'C', 'H', 'H', 'H']
        coords = [
            [0.000000000000, 0.000000000000, 0.000000000000],
            [0.000000000000, 0.000000000000, 1.498047000000],
            [0.000000000000, -0.938765985000, 2.004775984000],
            [0.000000000000, 0.938765985000, 2.004775984000],
            [-0.744681452, -0.131307432, -0.634501434]
        ]

        n_orbs_active = 3
        n_elec_active = 4
        charge = 0
        multiplicity = 1
        basis = "sto-3g"
        problem = saoovqe.ProblemSet(symbols, coords, charge, multiplicity,
                                     n_elec_active, n_orbs_active, basis)
        initial_circuits = (
            saoovqe.circuits.OrthogonalCircuitSet.from_problem_set(
                n_states, problem))
        ansatz = saoovqe.ansatz.Ansatz.from_problem_set(
            saoovqe.AnsatzType.GUCCSD, problem,
            repetitions,
            qubit_mapper=problem.fermionic_mapper)
        saoovqe_solver = saoovqe.vqe_optimization.SAOOVQE(estimator,
                                                          initial_circuits,
                                                          ansatz,
                                                          problem,
                                                          orbital_optimization_settings={})
        energies = saoovqe_solver.get_energy(
            SciPyOptimizer('SLSQP', options={'maxiter': 500, 'ftol': 1e-8}))

        print(f'params:\n{saoovqe_solver.ansatz_param_values}')
        print(f'engs:\n{energies}')

        ref_params = np.array(
            [0.36802972, 0.17568437, 0.36767911, 0.17565869, 0.24262702,
             0.24380789, 0.03073291,
             0.10321177, 0.14960804, 0.02928037, 0.08329617, -0.04767951,
             0.15190259, -0.04838016,
             0.01288679])

        # Permute to take into account different ordering of single
        # excitation during ansatz creation

        ref_params[[2, 3, 4]] = ref_params[[4, 2, 3]]

        # Testing absolute value to take into account difference in ansatz
        # signs for double excitations

        assert np.allclose(np.abs(saoovqe_solver.ansatz_param_values),
                           np.abs(ref_params),
                           atol=1e-2)
        assert np.allclose(energies, [-92.75359259758139, -92.73271983153884])

        # Store the solver into Pytest namespace
        pytest.solver_oo_4_3 = saoovqe_solver

    @pytest.mark.dependency(depends=['test_get_energy_with_oo_4_3'])
    def test_eval_eng_gradient_with_oo_4_3(self):
        """
        Testing gradients for all atoms and the first two doublet states
        w.r.t. reference values with
        orbital-optimization. The active space is enlarged to 3 molecular
        orbitals containing 4 electrons.
        """

        grad_results = np.array([[[-0.1260276749714621, -0.15380364947448583,
                                   -0.23925711091732624],
                                  [0.046299748047505127, 0.05688444944663793,
                                   0.24550347593247968],
                                  [0.024593829242473803, 0.022791884500965975,
                                   -0.030703011660954273],
                                  [-0.04173188676333546, -0.026566123925686424,
                                   -0.011076533159043287],
                                  [0.09686598444482074, 0.10069343945259437,
                                   0.03553317980445671]],
                                 [[-0.11731262728648938, 0.09658874534998224,
                                   -0.23586522338071106],
                                  [0.0429900775257466, -0.04291390043880168,
                                   0.22679310662690846],
                                  [-0.03955610493791329, 0.026635557090157497,
                                   -0.0124871889834652],
                                  [0.019249695017991245, -0.022862518452430945,
                                   -0.02725401299743999],
                                  [0.09462895968065811, -0.057447883548923044,
                                   0.04881331873443468]]])

        for state_idx in range(2):
            for atom_idx in range(5):
                assert np.allclose(
                    pytest.solver_oo_4_3.eval_eng_gradient(state_idx,
                                                           atom_idx),
                    grad_results[state_idx][atom_idx],
                    atol=1e-2)

    @pytest.mark.dependency(depends=['test_eval_eng_gradient_with_oo_4_3'])
    def test_eval_nac_with_oo_4_3(self):
        """
        Testing computation of non-adiabatic couplings with all molecular
        orbitals optimized and after get_energy() and
        eval_eng_gradient() manually called. The active space is enlarged to
        3 molecular orbitals containing 4
        electrons.
        """

        nac_ci_results = np.array(
            [[4.367201184224496, -0.4342347015491995, -6.108729725719978],
             [-0.5118421369215879, 0.2870703285837414, 5.655454660263247],
             [-0.6420770792525687, 0.15652521634749447, -0.3806844771910736],
             [-0.33953005240249357, -0.17354925830007786, -0.282070134915375],
             [-2.873751915648927, 0.16418841491665642, 1.1160296775650262]])

        nac_csf_results = np.array([[0.049278358224529355, -0.2731903056993118,
                                     0.0019032721554248684],
                                    [-0.0003345766254203965,
                                     0.03404628862060875,
                                     0.0003892503140111303],
                                    [-0.019379051207143665,
                                     0.0011802046267190434,
                                     0.0030007375458930307],
                                    [0.0171773067904876, 0.0011204093953391262,
                                     -0.002946726588592907],
                                    [-0.008670278311177459,
                                     0.06092704015782809,
                                     -0.0018873854808269415]])

        for atom_idx in range(5):
            pytest.solver_oo_4_3.eval_nac(atom_idx)
            assert np.allclose(-pytest.solver_oo_4_3.ci_nacs[atom_idx],
                               nac_ci_results[atom_idx], atol=5e-1)
            assert np.allclose(-pytest.solver_oo_4_3.csf_nacs[atom_idx],
                               nac_csf_results[atom_idx], atol=1e-3)

    def test_get_energy_dHab(self):
        """
        Testing resulting energies w.r.t. reference values without orbital
        optimization.
        """
        estimator = Estimator()
        sampler = Sampler()
        n_states = 2
        repetitions = 1
        symbols = ['N', 'C', 'H', 'H', 'H']
        coords = [
            [0.000000000000, 0.000000000000, 0.000000000000],
            [0., 0., -1.412052],
            [0., -0.94421526, -1.93740123],
            [0., 0.94421526, -1.93740123],
            [0.92571167, 0.24804369, 0.34107453]
        ]

        n_orbs_active = 3
        n_elec_active = 4
        charge = 0
        multiplicity = 1
        basis = 'cc-pVDZ'
        load_wfn = psi4.core.Wavefunction.from_file(f'{Path(__file__).parent}/../example/diabatization/diabatic_CAS43_ccpVDZ_phi0_theta180_NoZmatrix')
        problem = saoovqe.ProblemSet.with_dia_orbs_from_prev_wfn(symbols, coords, charge, multiplicity, n_elec_active,
                                                                 n_orbs_active, load_wfn, basis)
        initial_circuits = (
            saoovqe.circuits.OrthogonalCircuitSet.from_problem_set(
                n_states, problem))
        ansatz = saoovqe.ansatz.Ansatz.from_problem_set(
            saoovqe.AnsatzType.GUCCSD, problem,
            repetitions,
            qubit_mapper=problem.fermionic_mapper)

        saoovqe_solver = saoovqe.SAOOVQE(estimator=estimator,
                                         initial_circuits=initial_circuits,
                                         ansatz=ansatz,
                                         problem=problem,
                                         sampler=sampler,
                                         orbital_optimization_settings={})

        energies = saoovqe_solver.get_energy(
            (SciPyOptimizer('SLSQP', options={'maxiter': 1000, 'ftol': 1e-9})))

        pytest.solver = saoovqe_solver

        assert np.allclose(energies,
                           [-93.976931678,    -93.931562783],
                           atol=1e-3)


    @pytest.mark.dependency(depends=['test_get_energy_dHab'])
    def test_dHab(self):
        pytest.solver.eval_dHab(4)
        dHab_xyz = pytest.solver.dHab[4]

        assert np.allclose( dHab_xyz,
                            [-0.022466493, 0.005001270,  0.031562394],
                            atol=1e-3)

    @pytest.mark.dependency(depends=['test_get_energy_dHab'])
    def test_overlap(self):
        phiA_psiA = pytest.solver.eval_state_overlap(pytest.solver.optimized_state_circuits[0],
                                                     pytest.solver.initial_circuits[0])
        phiB_psiA = pytest.solver.eval_state_overlap(pytest.solver.optimized_state_circuits[0],
                                                     pytest.solver.initial_circuits[1])
        phiA_psiB = pytest.solver.eval_state_overlap(pytest.solver.optimized_state_circuits[1],
                                                     pytest.solver.initial_circuits[0])
        phiB_psiB = pytest.solver.eval_state_overlap(pytest.solver.optimized_state_circuits[1],
                                                     pytest.solver.initial_circuits[1])

        assert np.allclose([phiA_psiA, phiB_psiA, phiA_psiB, phiB_psiB],
                           [-0.741974480,     -0.556511689,      0.594508478,     -0.681833657],
                           atol=1e-3)
