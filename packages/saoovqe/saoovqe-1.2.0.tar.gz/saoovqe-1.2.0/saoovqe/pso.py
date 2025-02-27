"""Module implementing Particle Swarm Optimization method."""

from typing import Callable

import numpy as np
from qiskit_algorithms.optimizers import OptimizerResult, OptimizerSupportLevel
from sklearn.cluster import DBSCAN


class PSOOptimizer:
    """
    Class implementing Particle Swarm Optimization method.
    """

    def __init__(
        self,
        maxiter=1000,
        use_stencil=False,
        stencil_type="none",
        stencil_diff=1e-3,
        choose_value_from_stencil="original",
        velocity_convergence=1e-6,
        num_avg_res=1,
        max_inertia=0.7,
        min_inertia=0.2,
        cognitive_coeff=0.4,
        social_coeff=0.6,
        lbound=-10,
        ubound=10,
        cluster_treshold=1,
    ):
        # TODO specify maxevals as the next parameter???
        super().__init__()

        self._maxiter = maxiter
        self._use_stencil = use_stencil
        self._stencil_type = stencil_type
        self._stencil_diff = stencil_diff
        self._choice_type = choose_value_from_stencil
        self._velocity_convergence = velocity_convergence
        self._num_avg_res = num_avg_res
        self._max_inertia = max_inertia
        self._min_inertia = min_inertia
        self._cognitive_coeff = cognitive_coeff
        self._social_coeff = social_coeff
        self._lbound = lbound
        self._ubound = ubound
        self._cluster_treshold = cluster_treshold

    def get_support_level(self):
        """
        Optimizer properties (i.e. "support level") specification.
        """

        return {
            "gradient": OptimizerSupportLevel.ignored,
            "bounds": OptimizerSupportLevel.required,
            "initial_point": OptimizerSupportLevel.required,
        }

    def _pso_update_best(self, best_x, best_y, particle_best_x, particle_best_y):
        for i, e in enumerate(particle_best_y):
            if e < best_y:
                best_x = particle_best_x[i]
                best_y = e

        return best_x, best_y

    def _pso_check_bounds(self, position):
        position[position > self._ubound] = np.random.default_rng().uniform(
            self._lbound, self._ubound, position[position > self._ubound].shape
        )
        position[position < self._lbound] = np.random.default_rng().uniform(
            self._lbound, self._ubound, position[position < self._lbound].shape
        )

    def _get_stencil_values(self, fun, coord):
        dimension = len(coord)

        values = fun(coord)
        stencil_values = np.array([])

        if self._stencil_type == "symmetric":
            stencil_values = np.zeros(dimension * 2)

            for i in range(dimension):
                coord_plus = coord.copy()
                coord_minus = coord.copy()
                coord_plus[i] += self._stencil_diff
                coord_minus[i] -= self._stencil_diff
                stencil_values[2 * i] = fun(coord_plus)
                stencil_values[2 * i + 1] = fun(coord_minus)

        elif self._stencil_type == "minus":
            stencil_values = np.zeros(dimension)

            for i in range(dimension):
                coord_minus = coord.copy()
                coord_minus[i] -= self._stencil_diff
                stencil_values[i] = fun(coord_minus)

        elif self._stencil_type == "plus":
            stencil_values = np.zeros(dimension)

            for i in range(dimension):
                coord_plus = coord.copy()
                coord_plus[i] += self._stencil_diff
                stencil_values[i] = fun(coord_plus)

        elif self._stencil_type == "random_side":
            stencil_values = np.zeros(dimension)

            for i in range(dimension):
                coord_new = coord.copy()
                coord_new[i] += ((-1) ** np.random.randint(1, 3)) * self._stencil_diff
                stencil_values[i] = fun(coord_new)
        elif self._stencil_type == "none":
            stencil_values = np.array([])

        all_values = np.append(values, stencil_values)

        return all_values

    def _choose_from_stencil(self, values):
        if self._choice_type == "min":
            return min(values)

        if self._choice_type == "average":
            return np.sum(values) / len(values)

        return values[0]

    def _pso(self, fun, x0):
        dimension = len(x0)

        n_particles = dimension * 10
        gbest_x = x0
        gbest_y = fun(x0)

        particles = np.random.default_rng().uniform(
            self._lbound, self._ubound, (n_particles, dimension)
        )
        particles[0, :] = x0

        particle_best_x = np.copy(particles)
        particle_best_y = np.zeros(n_particles)
        velocity = np.random.default_rng().uniform(
            -self._ubound, self._ubound, (n_particles, dimension)
        )

        for i in range(n_particles):
            particle_best_y[i] = fun(particles[i])

        particle_y = np.copy(particle_best_y)
        gbest_x, gbest_y = self._pso_update_best(
            gbest_x, gbest_y, particle_best_x, particle_best_y
        )

        iteration = 0
        converged = False
        while iteration < self._maxiter and not converged:
            inertia = (self._max_inertia - self._min_inertia) / (self._maxiter - 1) * (
                self._maxiter - 1 - iteration
            ) + self._min_inertia
            velocity = (
                inertia * velocity
                + self._cognitive_coeff
                * np.random.default_rng().uniform(0, 1, (n_particles, dimension))
                * (particle_best_x - particles)
                + self._social_coeff
                * np.random.default_rng().uniform(0, 1, (n_particles, dimension))
                * (gbest_x - particles)
            )
            particles += velocity
            self._pso_check_bounds(particles)

            for i in range(n_particles):
                if self._use_stencil:
                    particle_y[i] = self._choose_from_stencil(
                        self._get_stencil_values(fun, particles[i])
                    )
                else:
                    particle_y[i] = fun(particles[i])
                if particle_y[i] < particle_best_y[i]:
                    particle_best_y[i] = particle_y[i]
                    particle_best_x[i] = particles[i]

            gbest_x, gbest_y = self._pso_update_best(
                gbest_x, gbest_y, particle_best_x, particle_best_y
            )

            iteration += 1
            cluster = DBSCAN(eps=0.1, min_samples=2).fit(particles)
            cluster_labels = cluster.labels_
            clustered = cluster_labels == -1

            if (
                np.sum(clustered) < self._cluster_treshold
                and np.max(velocity) < self._velocity_convergence
            ):
                converged = True

        test_avg = 0
        for i in range(self._num_avg_res):
            test_avg += fun(gbest_x)

        test_avg /= self._num_avg_res

        gbest_y = min(gbest_y, test_avg)

        result = OptimizerResult()
        result.x = gbest_x
        result.fun = gbest_y
        result.nfev = iteration * n_particles * (dimension + 1) + 1 + self._num_avg_res
        result.njev = None
        result.nit = iteration

        return result

    def minimize(self, fun: Callable, x0: np.ndarray) -> OptimizerResult:
        """
        Function to run Particle Swarm Optimization method.

        :param fun: Objective function (to be optimized)
        :param x0: Initial point coordinates
        :return: Result of the optimization
        """
        return self._pso(fun, x0)
