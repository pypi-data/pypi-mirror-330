"""
Tests for psi4 settings.
"""
import logging
import sys
from pathlib import Path

import numpy as np
import saoovqe
import pickle

# Set the global logger to ERROR level, so that the outputs except errors won't be printed
log = logging.getLogger('SAOOVQE.logger')
log.setLevel(logging.ERROR)

sys.setrecursionlimit(20000)

class TestPsi4:
    """
    Tests for psi4 settings.
    """
    def test_psi4_integral_coeff_ordering(self):
        """
        Testing if the integral coefficient ordering is correct. I.e. chemist vs physicist notation.
        """

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

        with open(f'{Path(__file__).resolve().parent.parent}/'
                                                    f'tests/full_ham_two_body_integrals_mo.pickle', 'rb') as f:
            full_ham_mo_test = pickle.load(f)

        print(full_ham_mo_test)

        assert np.allclose(full_ham_mo_test, problem.full_ham_two_body_integrals_mo[0])

