import numpy as np
import matplotlib.pyplot as plt
from sympy import *

def perturb_points(x, perturbation_bound=1.0, sphere_dist="uniform", length_dist="uniform"):
    rng = np.random.default_rng()
    n = len(x[0])
    m = len(x)
    if sphere_dist == "uniform":
        sphere_dist = [rng.multivariate_normal(np.zeros(n), np.eye(n)) for i in range(m)]
        sphere_dist = [entry/np.linalg.norm(entry) for entry in sphere_dist]
    if length_dist == "uniform":
        length_dist = rng.uniform(0,perturbation_bound,m)
    perturbations = [sphere_dist[i]*length_dist[i] for i in range(m)]
    result = [x[i] + perturbations[i] for i in range(m)]
    return np.array(result)
