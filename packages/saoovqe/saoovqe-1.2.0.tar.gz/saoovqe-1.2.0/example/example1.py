#%% md
# # Example 1: Computation of Energies and Gradients
# 
# In this example it is shown, how to run the basic energy and gradient computations. Also, the results are compared to
# CASSCF implementation provided by Psi4 package.
#%% md
# Firstly, we specify geometry of the system given in Cartesian coordinates.
#%%
symbols = ['N', 'C', 'H', 'H', 'H']
coords = [
    [0.000000000000, 0.000000000000, 0.000000000000],
    [0.000000000000, 0.000000000000, 1.498047000000],
    [0.000000000000, -0.938765985000, 2.004775984000],
    [0.000000000000, 0.938765985000, 2.004775984000],
    [-0.744681452, -0.131307432, -0.634501434]
]
#%% md
# Subsequently, we specify the system properties.
#%%
n_orbs_active = 2
n_elec_active = 2
charge = 0
multiplicity = 1
basis = 'sto-3g'
#%% md
# Now we construct a `ProblemSet` instance containing the information about our electronic structure problem.
#%%
import saoovqe
import psi4
#%%
saoovqe.__version__
#%%

problem = saoovqe.problem.ProblemSet(
    symbols=symbols,
    coords=coords,
    charge=charge,
    multiplicity=multiplicity,
    n_electrons_active=n_elec_active,
    n_orbitals_active=n_orbs_active,
    basis_name=basis
)
#%% md
# The next one is a set of circuits representing orthogonal states used to construct the whole circuits
# representing state vectors later.
#%%
import numpy as np
test1 = problem.qubit_active_hamiltonian.to_matrix()

min(np.linalg.eig(test1)[0])
#%%
initial_circuits = saoovqe.OrthogonalCircuitSet.from_problem_set(n_states=2, problem=problem)
#%% md
# Another ingredient for statevector circuits constructed later will be an ansatz.
#%%
ansatz = saoovqe.Ansatz.from_ProblemSet(ansatz=saoovqe.AnsatzType.GUCCSD,
                                               problem=problem,
                                               repetitions=1,
                                               qubit_mapper=problem.fermionic_mapper)
#%% md
# Now we can create an instance of our SA-OO-VQE solver. Orbital-optimization doesn't have to be used,
# but we do use it here, to compare with CASSCF.
#%%
from qiskit.primitives import Estimator

estimator = Estimator()

solver = saoovqe.SAOOVQE(estimator=estimator,
                         initial_circuits=initial_circuits,
                         ansatz=ansatz,
                         problem=problem,
                         orbital_optimization_settings={})
#%% md
# Let's create a numerical optimizer, pass it to our solver and compute our energies now.
#%%
from qiskit_algorithms.optimizers import SciPyOptimizer

optimizer = SciPyOptimizer('SLSQP', options={'maxiter': 500, 'ftol': 1e-8})
saoovqe_engs = solver.get_energy(optimizer)

print(saoovqe_engs)
#%% md
# Also, without further setting things up, we're ready to compute our gradients now!
#%%
import numpy as np
test1 = problem.qubit_active_hamiltonian.to_matrix()

np.linalg.eig(test1)[0]
#%%
saoovqe_grads = []
for state_idx in range(2):
    saoovqe_grads.append(list())
    for atom_idx in range(len(coords)):
        grad = solver.eval_eng_gradient(state_idx, atom_idx)
        print(grad)
        saoovqe_grads[state_idx].append(grad)
#%% md
# Perfect! For now, let's set our Psi4 CASSCF solver up. Let's start with re-writing our geometry specification in Psi4-convenient
# way and passing it to the toolkit.
#%%
import psi4
import numpy as np

def gen_formaldimine_geom_psi4(alpha, phi):
    variables = [1.498047, 1.066797, 0.987109, 118.359375, alpha, phi]

    # Create Z-matrix
    string_geo_dum = '''0 1
                    N
                    C 1 {0}
                    H 2 {1}  1 {3}
                    H 2 {1}  1 {3} 3 180
                    H 1 {2}  2 {4} 3 {5}
                    symmetry c1
                    '''.format(*variables)

    # Convert to Cartesian coordinates
    psi4.core.set_output_file('out.txt', False)
    molecule_dum = psi4.geometry(string_geo_dum)
    molecule_dum.translate(psi4.core.Vector3(-molecule_dum.x(0), -molecule_dum.y(0), -molecule_dum.z(0)))
    mol_geom_dum = molecule_dum.geometry().np * problem.unit_constants['Bohr_to_Angstrom']

    if not np.isclose(mol_geom_dum[1, 1], 0.):
        mol_geom_dum[:, [1, 2]] = mol_geom_dum[:, [2, 1]]
        mol_geom_dum[4, 0] = -mol_geom_dum[4, 0]

    string_geo = ''
    for i, e in enumerate(mol_geom_dum):
        string_geo += f'{molecule_dum.flabel(i)}, {e[0]}, {e[1]}, {e[2]}\n'

    string_geo += 'symmetry c1\n' \
                  'nocom\n' \
                  'noreorient\n'

    return string_geo

psi4.geometry(gen_formaldimine_geom_psi4(130, 80))
#%%
gen_formaldimine_geom_psi4(130, 80)
#%% md
# Now we'll specify all options for Psi4 CASSCF solver.
#%%
problem._active_space_transformer.prepare_active_space(16,13, occupation_alpha=None, occupation_beta=None)
#%%
n_orbs_frozen = len(problem.frozen_orbitals_indices)

def psi4_casscf():
    psi4.set_options({'basis': basis,
                      'DETCI_FREEZE_CORE': False,
                      'reference': 'RHF',
                      'scf_type': 'pk',
                      'num_roots': len(initial_circuits),
                      'frozen_docc': [0],
                      'restricted_docc': [n_orbs_frozen],
                      'active': [n_orbs_active],
                      'restricted_uocc': [solver.n_mo_optim - n_orbs_frozen - n_orbs_active],
                      'frozen_uocc': [problem.virtual_orbitals_indices[-1] - solver.n_mo_optim + 1],
                      'MAXITER': 1000,
                      'DIIS': False,
                      'D_CONVERGENCE': 1e-6,
                      'E_CONVERGENCE': 1e-6,
                      'S': 0,
                      'avg_states': [0, 1],
                      'avg_weights': [0.5, 0.5]})
    psi4.energy('scf', return_wfn=True)
    psi4.energy('casscf', return_wfn=True)
#%% md
# And run CASSCF preceded by a common SCF computation!
#%%
psi4.variable("CURRENT DIPOLE")
#%%
saoovqe_engs
#%%
psi4_casscf()

psi4_eng0 = psi4.variable('CI ROOT 0 TOTAL ENERGY')
psi4_eng1 = psi4.variable('CI ROOT 1 TOTAL ENERGY')
#%% md
# Cool! Now we can check, if they're similar to our SA-OO-VQE-obtained energies...
#%%
print(psi4_eng0 - saoovqe_engs[0])
print(psi4_eng1 - saoovqe_engs[1])
#%% md
# Congratulations! Now it seems, that our energies are really close. Let's compute some gradients
# via Psi4. In this case, we'll stick to simple stuff and utilize finite-differences approach.
# Specifically, we'll obtain derivatives w.r.t. the $\alpha$ angle. So, first of all, let's generate
# shifted geometries.
#%%
delta = 1e-5

geom_plus = gen_formaldimine_geom_psi4(alpha=130+(delta/2), phi=80)
geom_minus = gen_formaldimine_geom_psi4(alpha=130-(delta/2),phi=80)
#%% md
# With geometries prepared, we can evaluate the corresponding energies.
#%%
psi4.geometry(geom_plus)
psi4_casscf()
psi4_eng0_plus = psi4.variable('CI ROOT 0 TOTAL ENERGY')
psi4_eng1_plus = psi4.variable('CI ROOT 1 TOTAL ENERGY')

psi4.geometry(geom_minus)
psi4_casscf()
psi4_eng0_minus = psi4.variable('CI ROOT 0 TOTAL ENERGY')
psi4_eng1_minus = psi4.variable('CI ROOT 1 TOTAL ENERGY')
#%% md
# And finally, let's evaluate Psi4 gradients w.r.t. $\alpha$.
#%%
psi4_grad_0 = (psi4_eng0_plus - psi4_eng0_minus)/delta
psi4_grad_1 = (psi4_eng1_plus - psi4_eng1_minus)/delta
#%% md
# The gradients obtained directly from SA-OO-VQE are evaluated w.r.t. Cartesian coordinates, so we'll transform
# these to internal coordinate system to be able to compare the results to each other.
#%%
def cartesian_to_inner(vector, R, phi, alpha):
    phi_rad = np.deg2rad(phi)
    alpha_rad = np.deg2rad(alpha)
    v_R = -(vector[0] * np.sin(phi_rad) * np.sin(alpha_rad)) - (vector[1] * np.cos(phi_rad) * np.sin(alpha_rad)) + (vector[2] * np.cos(alpha_rad))
    v_phi = -(vector[0] * R * np.cos(phi_rad) * np.sin(alpha_rad)) + (vector[1] * R * np.sin(phi_rad) * np.sin(alpha_rad))
    v_alpha = -(vector[0] * R * np.sin(phi_rad) * np.cos(alpha_rad)) - (vector[1] * R * np.cos(phi_rad) * np.cos(alpha_rad)) \
              - (vector[2] * R * np.sin(alpha_rad))

    return np.pi * np.array([v_R , v_phi, v_alpha]) / 180

bond_length = np.sqrt(sum(np.array(coords[4])**2))
saoovqe_grad_0_inner = cartesian_to_inner(saoovqe_grads[0][4], bond_length, 80, 130)
saoovqe_grad_1_inner = cartesian_to_inner(saoovqe_grads[1][4], bond_length, 80, 130)

print(saoovqe_grad_0_inner[2])
print(saoovqe_grad_1_inner[2])
print(psi4_grad_0)
print(psi4_grad_1)
#%% md
# And bingo! Even the gradients seem pretty close, so they're hopefully correct :D