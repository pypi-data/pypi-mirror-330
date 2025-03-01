import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Tuple, List, Dict, Optional
import random
import multiprocessing
import sys

class SierpinskiHPO:
    def __init__(self, param_ranges: Dict[str, Tuple[float, float]], 
                 objective_function: Callable, 
                 max_iterations: int = 50,
                 max_depth: int = 5,
                 minimize: bool = False,
                 use_adaptive_threshold: bool = True,
                 use_parallel: bool = True,
                 use_random_sampling: bool = True,
                 warm_start: Optional[List[Tuple[Dict[str, float], float]]] = None):
        self.param_ranges = param_ranges
        self.objective_function = objective_function
        self.max_iterations = max_iterations
        self.max_depth = max_depth
        self.minimize = minimize
        self.use_adaptive_threshold = use_adaptive_threshold
        
        # Disable multiprocessing if running in Jupyter/Colab
        self.use_parallel = use_parallel and ("ipykernel" not in sys.modules)
        self.use_random_sampling = use_random_sampling

        self.evaluations = 0
        self.results = warm_start if warm_start else []
        self.best_params = None
        self.best_score = float('inf') if minimize else float('-inf')

        self.param_names = list(param_ranges.keys())
        self.size = 1.0

    def _evaluate(self, params: Dict[str, float]) -> float:
        score = self.objective_function(params)
        self.results.append((params, score))
        self.evaluations += 1

        if (self.minimize and score < self.best_score) or (not self.minimize and score > self.best_score):
            self.best_score = score
            self.best_params = params.copy()
        return score

    def _adaptive_threshold(self) -> float:
        return 0.9 - 0.3 * (self.evaluations / self.max_iterations)

    def _is_promising_region(self, scores: List[float]) -> bool:
        threshold = self._adaptive_threshold() if self.use_adaptive_threshold else 0.7
        if self.minimize:
            return min(scores) <= self.best_score + threshold * (max(s for _, s in self.results) - self.best_score)
        else:
            return max(scores) >= self.best_score - threshold * (self.best_score - min(s for _, s in self.results))

    def _get_random_vertex(self, vertices):
        return {k: (vertices[0][k] + vertices[1][k] + vertices[2][k]) / 3 + random.uniform(-0.1, 0.1) for k in vertices[0]}

    def _recursive_search(self, depth: int, vertices: List[Dict[str, float]]):
        if self.evaluations >= self.max_iterations or depth >= self.max_depth:
            return

        vertex_scores = [self._evaluate(vertex) for vertex in vertices]

        if not self._is_promising_region(vertex_scores):
            return

        midpoints = [{k: (vertices[i][k] + vertices[(i+1) % 3][k]) / 2 for k in vertices[0]} for i in range(3)]
        
        sub_triangles = [
            [vertices[0], midpoints[0], midpoints[2]],
            [midpoints[0], vertices[1], midpoints[1]],
            [midpoints[2], midpoints[1], vertices[2]]
        ]

        if self.use_random_sampling:
            sub_triangles.append([midpoints[0], midpoints[1], midpoints[2], self._get_random_vertex(vertices)])

        if self.use_parallel:
            with multiprocessing.Pool(3) as pool:
                pool.starmap(self._recursive_search, [(depth + 1, sub) for sub in sub_triangles])
        else:
            for sub in sub_triangles:
                self._recursive_search(depth + 1, sub)

    def optimize(self) -> Tuple[Dict[str, float], float]:
        initial_triangle = [
            {name: 0.0 for name in self.param_names},
            {name: 1.0 for name in self.param_names},
            {name: 0.5 for name in self.param_names}
        ]
        initial_triangle[2][self.param_names[1]] = 1.0 if len(self.param_names) > 1 else 0.5
        self._recursive_search(0, initial_triangle)
        return self.best_params, self.best_score

    def plot_search(self):
        if len(self.param_names) < 2:
            print("Cannot visualize: Need at least 2 parameters")
            return

        plt.figure(figsize=(10, 8))
        xs, ys, scores = zip(*[(p[self.param_names[0]], p[self.param_names[1]], s) for p, s in self.results])
        plt.scatter(xs, ys, c=scores, cmap='viridis', s=50, alpha=0.7)
        plt.colorbar(label='Objective Value')
        plt.title("Sierpinski HPO Search Pattern")
        plt.xlabel(self.param_names[0])
        plt.ylabel(self.param_names[1])
        plt.show()
