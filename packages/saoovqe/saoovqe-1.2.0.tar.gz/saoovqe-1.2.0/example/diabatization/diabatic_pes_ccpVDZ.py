#!/usr/bin/env python3
"""
Example script for utilization of SA-OO-VQE solver on the computation of formaldimine (methylene imine) molecule
energies for the lowest 2 singlet states, gradients of the potential energy surface and the corresponding non-adiabatic
couplings.
"""
import numpy as np
from qiskit_algorithms.optimizers import SciPyOptimizer
from qiskit.primitives import Estimator, Sampler
import psi4
import sys
import saoovqe

def run_sacasscf_psi4(string_geo,
                      basisset,
                      n_mo_optimized,
                      active_indices,
                      frozen_indices,
                      virtual_indices,
                      num_roots,
                      avg_states,
                      avg_weights,
                      orbital_optimize=True,
                      output=False,
                      d_conv=1e-6,
                      e_conv=1e-6):
    """
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    Function to perform SA-CASSCF with psi4.
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    """
    frozen_uocc = virtual_indices[-1] - n_mo_optimized + 1
    restricted_uocc = n_mo_optimized - \
        (len(frozen_indices) + len(active_indices))

    options = {'basis': basisset,
               'DETCI_FREEZE_CORE': False,
               'reference': 'RHF',
               'scf_type': 'pk',  # set e_convergence and d_convergence to 1e-8 instead of 1e-6
               'num_roots': num_roots,
               'frozen_docc': [0],
               'restricted_docc': [len(frozen_indices)],
               'active': [len(active_indices)],
               'restricted_uocc': [restricted_uocc],
               'frozen_uocc': [frozen_uocc],
               'MAXITER': 1000,
               'DIIS': False,
               'D_CONVERGENCE': d_conv,
               'E_CONVERGENCE': e_conv,
               'S' : 0}
    options['avg_states'] = avg_states
    options['avg_weights'] = avg_weights

    psi4.geometry(string_geo)
    psi4.set_options(options)

    if output is not False: 
       psi4.core.set_output_file(output,False)

    psi4.energy('scf', return_wfn=True)
    if orbital_optimize:
     psi4.energy('casscf', return_wfn=True)
    else:
     psi4.energy('fci', return_wfn=True)
    
    if num_roots > 1:
      energies = []
      for root in range(num_roots):
        energies.append(psi4.variable('CI ROOT {} TOTAL ENERGY'.format(root)))
      return energies
    else:
        energy = psi4.variable('CI TOTAL ENERGY')
        return [energy]

R_BOHR_ANG = 0.5291772105638411

# Transform sa-oo-vqe gradients to spherical coordinates
def grad_vec_to_spherical(vector, R, phi, theta):
    phi_rad = np.deg2rad(phi)
    theta_rad = np.deg2rad(theta)
    v_R = (vector[0] * np.cos(phi_rad) * np.sin(theta_rad)) + (
        vector[1] * np.sin(phi_rad) * np.sin(theta_rad)) - (
            vector[2] * np.cos(theta_rad))
    v_phi = R*(- vector[0] * np.sin(phi_rad) * np.sin(theta_rad) + 
        vector[1] * np.cos(phi_rad) * np.sin(theta_rad))
    v_theta = R*(vector[0] * np.cos(phi_rad) * np.cos(theta_rad) +
        vector[1] * np.sin(phi_rad) * np.cos(theta_rad) +
            vector[2] * np.sin(theta_rad))
    return v_R, v_phi, v_theta

def no_Zmatrix_geometry(theta, phi):

    R = 1.017251
    PH = np.deg2rad(phi)
    TH = np.deg2rad(theta)
    X = R*np.sin(TH)*np.cos(PH)
    Y = R*np.sin(TH)*np.sin(PH)
    Z = -R*np.cos(TH) # avec un signe moins car TH est orienté en "mode pôle sud" et/ou PI-TH est le vrai angle polaire

    string_geo = """0 1
                    N                  0.00000000    0.00000000    0.00000000
                    C                  0.00000000    0.00000000   -1.41205200
                    H                  0.00000000   -0.94421526   -1.93740123
                    H                  0.00000000    0.94421526   -1.93740123
                    H                  {0}             {1}             {2}
                    symmetry c1
                    nocom
                    noreorient
                 """.format(X,Y,Z)

    molecule_geo = psi4.geometry(string_geo).geometry().np * R_BOHR_ANG
    geometry = [('N', molecule_geo[0]),
            ('C', molecule_geo[1]),
            ('H', molecule_geo[2]),
            ('H', molecule_geo[3]),
            ('H', molecule_geo[4])]

    return string_geo, geometry

#######################
# Method specification
#######################
estimator = Estimator()
sampler = Sampler()

n_states = 2
repetitions = 1

n_orbs_active = 3
n_elec_active = 4
charge = 0
multiplicity = 1
basis = "cc-pVDZ"

if basis=="sto-3g": nmo_total = 13
if basis=="cc-pVDZ": nmo_total = 43
if n_elec_active == 2: ncore = 7
if n_elec_active == 4: ncore = 6
frozen_indices    = [i for i in range(ncore)]
active_indices    = [i for i in range(ncore, 9)]
virtual_indices   = [i for i in range(9, nmo_total)]
n_mo_optimized    = virtual_indices[-1] + 1
num_roots         = 2
avg_states        = [0,1]
avg_weights       = [0.5,0.5]

R = 1.017251
theta_list = [180.0]
for npoints in range(18):
    theta_list.append(179.5902 - 5 * npoints)

load_wfn = psi4.core.Wavefunction.from_file("diabatic_CAS43_ccpVDZ_phi0_theta180_NoZmatrix")
#phi_list = [float(sys.argv[1])]
prev_coord = None

theta_list = [109.5902]
phi_list = [15]

for phi in phi_list:

    theta_list.reverse() # useful here if we use prev_coord and len(phi_list)>2 I guess.
    fname = f'diabatic_pes_{phi}.dat'

    f = open(fname,'w')
    f.write("{:>12s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} {:>16s} ".format("TH","E_A","E_B","H_AB","G_A_X","G_B_X","G_A_Y","G_B_Y","G_A_Z","G_B_Z","NAC_CI_X","NAC_CI_Y","NAC_CI_Z","NAC_CSF_X","NAC_CSF_Y","NAC_CSF_Z","<PhA|PsA>","<PhB|PsA>","<PhA|PsB>","<PhB|PsB>","dHab_dX","dHab_dY","dHab_dZ"))
    f.writelines("{:16s} ".format("psi4_E{}".format(item)) for item in range(num_roots))
    f.write("\n")
    f.close()

    for theta in theta_list:
        string_geo, geometry = no_Zmatrix_geometry(theta, phi)
        print(f'phi = {phi} and theta = {theta}\n')
        print(f'Geometry:\n {string_geo}')
        print(f'Geometry:\n {geometry}')
        symbols = [e[0] for e in geometry]
        coords = [e[1] for e in geometry]
#########################################################

# PSI4 reference:
        E_list = run_sacasscf_psi4(string_geo,
                                   basis,
                                   n_mo_optimized,
                                   active_indices,
                                   frozen_indices,
                                   virtual_indices,
                                   num_roots,
                                   avg_states,
                                   avg_weights,
                                   output="SACASSCF43_ccpVDZ_phi{}_theta{:.4f}.out".format(phi,theta),
                                   orbital_optimize=True)

# Weights of the ensemble:
        problem = saoovqe.ProblemSet.with_dia_orbs_from_prev_wfn(symbols, coords, charge, multiplicity, n_elec_active,
                                                                 n_orbs_active, load_wfn, basis)

# Step 1: Initialization - states |phiA>, |phiB>
        initial_circuits = saoovqe.OrthogonalCircuitSet.from_problem_set(n_states, problem)

# Define the ansatz circuit:
#
# Operator Û(theta)
        ansatz = saoovqe.Ansatz.from_problem_set(saoovqe.AnsatzType.GUCCSD,
                                        problem,
                                        repetitions,
                                        qubit_mapper=problem.fermionic_mapper)

# Perform SA-VQE procedure
        saoovqe_solver = saoovqe.SAOOVQE(estimator=estimator,
                                 initial_circuits=initial_circuits,
                                 ansatz=ansatz,
                                 problem=problem,
                                 sampler=sampler,
                                 orbital_optimization_settings={})

        E_A, E_B = saoovqe_solver.get_energy(SciPyOptimizer('SLSQP', options={'maxiter': 1000, 'ftol': 1e-9}),initial_ansatz_parameters=prev_coord, resolution_rotation=False)
        #prev_coord = saoovqe_solver.ansatz_param_values

        H_AB = saoovqe_solver.get_state_couplings(0,1)
        print(f'{phi} {theta} {E_A} {E_B} {H_AB} {saoovqe_solver.resolution_angle} {saoovqe_solver.ansatz_param_values}\n')

        grad_A_xyz = saoovqe_solver.eval_eng_gradient(0, 4)
        grad_B_xyz = saoovqe_solver.eval_eng_gradient(1, 4)
        grad_A_R, grad_A_phi, grad_A_theta = grad_vec_to_spherical(grad_A_xyz, R, phi, theta)
        grad_B_R, grad_B_phi, grad_B_theta = grad_vec_to_spherical(grad_B_xyz, R, phi, theta)

        NAC_TOT = saoovqe_solver.eval_nac(4)
        NAC_CI_xyz = saoovqe_solver.ci_nacs[4]
        NAC_CSF_xyz = saoovqe_solver.csf_nacs[4]
        dHab_eval = saoovqe_solver.eval_dHab(4)
        dHab_xyz = saoovqe_solver.dHab[4]
        NAC_CI_R, NAC_CI_phi, NAC_CI_theta = grad_vec_to_spherical(NAC_CI_xyz, R, phi, theta)
        NAC_CSF_R, NAC_CSF_phi, NAC_CSF_theta = grad_vec_to_spherical(NAC_CSF_xyz, R, phi, theta)
        dHab_R, dHab_phi, dHab_theta = grad_vec_to_spherical(dHab_xyz, R, phi, theta)

        phiA_psiA = saoovqe_solver.eval_state_overlap(saoovqe_solver.optimized_state_circuits[0],
                                                                  saoovqe_solver.initial_circuits[0])
        phiB_psiA = saoovqe_solver.eval_state_overlap(saoovqe_solver.optimized_state_circuits[0],
                                                                  saoovqe_solver.initial_circuits[1])
        phiA_psiB = saoovqe_solver.eval_state_overlap(saoovqe_solver.optimized_state_circuits[1],
                                                                  saoovqe_solver.initial_circuits[0])
        phiB_psiB = saoovqe_solver.eval_state_overlap(saoovqe_solver.optimized_state_circuits[1],
                                                                  saoovqe_solver.initial_circuits[1])


        f = open(fname,'a')
        f.write("{:>12.4f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} {:>16.9f} ".format(theta,E_A,E_B,H_AB,grad_A_xyz[0],grad_B_xyz[0],grad_A_xyz[1],grad_B_xyz[1],grad_A_xyz[2],grad_B_xyz[2],NAC_CI_xyz[0],NAC_CI_xyz[1],NAC_CI_xyz[2],NAC_CSF_xyz[0],NAC_CSF_xyz[1],NAC_CSF_xyz[2],phiA_psiA,phiB_psiA,phiA_psiB,phiB_psiB,dHab_xyz[0],dHab_xyz[1],dHab_xyz[2]))
        f.writelines("{:16.9f} ".format(item) for item in E_list)
        f.write("\n")
        f.close()
