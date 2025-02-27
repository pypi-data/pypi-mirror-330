"""Module for computation of QuantumCircuit gradients.

DEPRECATED: will be replaced by qiskit.algorithms.gradients in the future.
https://qiskit.org/documentation/stubs/qiskit.algorithms.gradients.html
#module-qiskit.algorithms.gradients
"""

from __future__ import annotations
from enum import Enum
import typing
from typing import Union
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.circuit.parametertable import ParameterView
from qiskit.circuit.parametervector import ParameterVectorElement

from .logger_config import log
from .circuits import OperatorEvaluatorBase

if typing.TYPE_CHECKING:
    from ansatz import Ansatz


class GradMethod(str, Enum):
    """
    Enumerator representing the type of gradient computation being used.
    """

    PARAMETER_SHIFT = "param_shift"
    FINITE_DIFF = "fin_diff"


class GradientEvaluator:
    """
    Class for gradient and Hessian computation.
    """

    def __init__(
        self,
        ansatz_circuit: Ansatz,
        op_evaluator: OperatorEvaluatorBase,
        deriv_params: (
            ParameterView[ParameterVectorElement]
            | list[Union[Parameter, ParameterVectorElement]]
        ),
        grad_method: GradMethod = GradMethod.PARAMETER_SHIFT,
        hess_method: GradMethod = GradMethod.PARAMETER_SHIFT,
    ):
        self._ansatz_circuit = ansatz_circuit
        self._op_evaluator = op_evaluator
        self._deriv_params = deriv_params
        self._grad_method = grad_method
        self._hess_method = hess_method

        # TODO make deltas parameters to be set up
        self._delta_grad = 1e-5 / 2.0
        self._delta_hess = 1e-5 / 2.0

        # Circuits for evaluation of gradient and Hessian
        #   Constructed when asked for, in a lazy loading manner.
        self._eval_func_no_deriv = self._op_evaluator.get_evaluation_func(
            self._ansatz_circuit
        )
        self._1_order_deriv_circs: Union[list[list[QuantumCircuit]], None] = None
        self._eval_funcs_ord_1: Union[list, None] = None
        self._2_order_deriv_circs: Union[list[list[QuantumCircuit]], None] = None
        self._eval_funcs_ord_2: Union[list, None] = None

        # Obtain Lagrange multipliers by solving
        # TODO extend for the all hessians and kappa coefficients after OO
        #  is implemented

        log.debug("GradientEvaluator was created.")

    @property
    def ansatz_circuit(self):
        """
        Ansatz quantum circuit
        """
        return self._ansatz_circuit

    @property
    def deriv_params(self):
        """
        The ansatz parameters. Derivatives are computed with respect to
        these parameters.
        """
        return self._deriv_params

    @property
    def grad_method(self) -> GradMethod:
        """
        Method chosen for gradient computation
        """
        return self._grad_method

    @property
    def hess_method(self) -> GradMethod:
        """
        Method chosen for Hessian computation
        """
        return self._hess_method

    def eval_grad(
        self, params: Union[list[float], tuple[float], np.ndarray]
    ) -> np.ndarray:
        """
        Evaluates gradient w.r.t. circuit parameters.

        :param params: Parameters to be passed into the circuit.
        :return: Gradient values
        """
        if not self._1_order_deriv_circs:
            self._construct_order_1_deriv_circs()

        return np.array(
            [
                self._central_diff_ord_1(func_pair[0](params), func_pair[1](params))
                for func_pair in self._eval_funcs_ord_1
            ]
        )

    def eval_hess(
        self, params: Union[list[float], tuple[float], np.ndarray]
    ) -> np.ndarray:
        """
        Evaluates Hessian w.r.t. circuit parameters.

        :param params: Parameters to be passed into the circuit.
        :return: Gradient values
        """
        if not self._2_order_deriv_circs:
            self._construct_order_2_deriv_circs()

        n_params = len(self._deriv_params)
        res = np.zeros((n_params, n_params))

        ord2_idx = 0
        for i in range(n_params):
            for j in range(i + 1):
                if self._deriv_params[i] == self._deriv_params[j]:
                    res[i][j] = self._central_diff_ord_2_same_var(
                        self._eval_funcs_ord_1[i][0](params),
                        self._eval_func_no_deriv(params),
                        self._eval_funcs_ord_1[i][1](params),
                    )
                else:
                    res[i][j] = self._central_diff_ord_2_diff_var(
                        self._eval_funcs_ord_2[ord2_idx][0](params),
                        self._eval_funcs_ord_1[i][0](params),
                        self._eval_funcs_ord_1[j][0](params),
                        self._eval_func_no_deriv(params),
                        self._eval_funcs_ord_1[i][1](params),
                        self._eval_funcs_ord_1[j][1](params),
                        self._eval_funcs_ord_2[ord2_idx][1](params),
                    )
                    ord2_idx += 1

        return res + res.T - np.diag(np.diag(res))

    def _construct_order_1_deriv_circs(self):
        self._1_order_deriv_circs = [
            [
                self._ansatz_circuit.assign_parameters(
                    {p: p + d_sign * self._delta_grad}
                )
                for d_sign in (1, -1)
            ]
            for p in self._deriv_params
        ]

        self._eval_funcs_ord_1 = [
            [self._op_evaluator.get_evaluation_func(c) for c in pair]
            for pair in self._1_order_deriv_circs
        ]

    def _construct_order_2_deriv_circs(self):
        # If not available, construct also circuits and evaluation functions
        # for 1st order derivatives,
        # as they're also being used here for second derivatives with
        # respect to the same variable
        if not self._1_order_deriv_circs:
            self._construct_order_1_deriv_circs()

        # Pairs of derivatives - corresponding parameters to be
        # differentiated togetger (d\dxdx, d\dxdy etc.)
        param_pairs = [
            (p1, p2)
            for i, p1 in enumerate(self._deriv_params)
            for p2 in self._deriv_params[i:]
            if p1 != p2
        ]

        # Constructing circuits for f(x + h, y + h, ...) and f(x - h, y - h,
        # ...)
        self._2_order_deriv_circs = [
            [
                self._ansatz_circuit.assign_parameters(
                    {p: p + d_sign * self._delta_grad for p in pair}
                )
                for d_sign in (1, -1)
            ]
            for pair in param_pairs
        ]

        self._eval_funcs_ord_2 = [
            [self._op_evaluator.get_evaluation_func(p) for p in pair]
            for pair in self._2_order_deriv_circs
        ]

    def _central_diff_ord_1(self, rshiftval: float, lshiftval: float) -> float:
        return (rshiftval - lshiftval) / (2 * self._delta_grad)

    def _central_diff_ord_2_same_var(
        self, rshiftval: float, fval: float, lshiftval: float
    ) -> float:
        return (rshiftval - 2 * fval + lshiftval) / self._delta_grad**2

    def _central_diff_ord_2_diff_var(
        self,
        rrshift: float,
        r1shift: float,
        r2shift: float,
        fval: float,
        l1shift: float,
        l2shift: float,
        llshift: float,
    ) -> float:
        return (
            rrshift - r1shift - r2shift + 2 * fval - l1shift - l2shift + llshift
        ) / (2 * self._delta_grad**2)
