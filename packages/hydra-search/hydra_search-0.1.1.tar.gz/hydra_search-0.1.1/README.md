# Hydra Search

Hydra Search is an advanced pathfinding algorithm inspired by the Hydra mechanism.

## Installation

```sh
pip install hydra-search
```

## Usage

```python
from hydra_search import HydraSearch

hsa = HydraSearch(search_space_size=100, num_searchers=10, parallel_mode='cpu')
best_section = hsa.run(iterations=10)
print("Best Section:", best_section)
```
