import numpy as np

from saoovqe.pso import PSOOptimizer


def ackley(x):
    return -20.0 * np.exp(
        -0.2 * np.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))) - np.exp(
        0.5 * (np.cos(2 * np.pi * x[0]) + np.cos(
            2 * np.pi * x[1]))) + np.e + 20


def rastrigin(x):
    return (x[0] ** 2 - 10 * np.cos(2 * np.pi * x[0])) + (
                x[1] ** 2 - 10 * np.cos(2 * np.pi * x[1])) + 20


def rosenbrock(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (x[0] - 1) ** 2


def sphere(x):
    return np.sum(np.array([x[i] ** 2 for i in range(len(x))]))


class TestPSO:
    """
    Tests the PSO class
    """

    def test_ackley(self):
        optimizer = PSOOptimizer(maxiter=10000,
                                 velocity_convergence=1e-5,
                                 num_avg_res=20,
                                 max_inertia=0.9,
                                 min_inertia=0.2,
                                 cognitive_coeff=0.4,
                                 social_coeff=0.6,
                                 lbound=-4,
                                 ubound=4)
        res = optimizer.minimize(ackley, x0=np.array([2, -2]))

        coordinates = res.x
        value = res.fun

        assert np.allclose(coordinates, np.array([0, 0]), atol=1e-4)
        assert np.allclose(value, 0, atol=1e-4)

    def test_rastrigin(self):
        optimizer = PSOOptimizer(maxiter=10000,
                                 velocity_convergence=1e-5,
                                 num_avg_res=20,
                                 max_inertia=0.9,
                                 min_inertia=0.2,
                                 cognitive_coeff=0.4,
                                 social_coeff=0.6,
                                 lbound=-5.12,
                                 ubound=5.12)
        res = optimizer.minimize(rastrigin, x0=np.array([2, 2]))
        coordinates = res.x
        value = res.fun

        assert np.allclose(coordinates, np.array([0, 0]), atol=1e-4)
        assert np.allclose(value, 0, atol=1e-4)

    def test_rosenbrock(self):
        optimizer = PSOOptimizer(maxiter=10000,
                                 velocity_convergence=1e-5,
                                 num_avg_res=20,
                                 max_inertia=0.9,
                                 min_inertia=0.2,
                                 cognitive_coeff=0.4,
                                 social_coeff=0.6,
                                 lbound=-5,
                                 ubound=10)
        res = optimizer.minimize(rosenbrock, x0=np.array([-4, 8]))
        coordinates = res.x
        value = res.fun

        assert np.allclose(coordinates, np.array([1, 1]), atol=1e-4)
        assert np.allclose(value, 0, atol=1e-4)

    def test_sphere(self):
        optimizer = PSOOptimizer(maxiter=10000,
                                 velocity_convergence=1e-5,
                                 num_avg_res=20,
                                 max_inertia=0.9,
                                 min_inertia=0.2,
                                 cognitive_coeff=0.4,
                                 social_coeff=0.6,
                                 lbound=-5.12,
                                 ubound=5.12)

        res = optimizer.minimize(sphere, x0=np.array(
            [-4, 4, -4, 4, -4, 4, -4, 4, -4, 4, -4, 4]))
        coordinates = res.x
        value = res.fun

        assert np.allclose(coordinates,
                           np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                           atol=1e-4)
        assert np.allclose(value, 0, atol=1e-4)
