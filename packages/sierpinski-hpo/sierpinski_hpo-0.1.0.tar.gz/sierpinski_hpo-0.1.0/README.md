# Sierpinski Hyperparameter Optimization (HPO)

This package implements the Sierpinski-based Hyperparameter Optimization algorithm.

## Installation
```
pip install -r requirements.txt
```

## Usage
Example usage of the optimizer:

```python
from sierpinski_hpo.sierpinski_hpo import SierpinskiHPO

def objective_function(params):
    x, y = params['x'], params['y']
    return -((x**2 + y - 11)**2 + (x + y**2 - 7)**2)

param_ranges = {'x': (-5, 5), 'y': (-5, 5)}
optimizer = SierpinskiHPO(param_ranges, objective_function, max_iterations=100, max_depth=6, minimize=False)
best_params, best_score = optimizer.optimize()

print(f"Best parameters: {best_params}, Best score: {best_score}")
optimizer.plot_search()
```

Run the example with:
```
python example.py
```

## Features
- Adaptive thresholding for promising regions
- Random sampling for better exploration
- Parallel evaluation (disabled in Jupyter)
- Improved high-dimensional mapping
- Early stopping for unpromising regions
- Visualization support
