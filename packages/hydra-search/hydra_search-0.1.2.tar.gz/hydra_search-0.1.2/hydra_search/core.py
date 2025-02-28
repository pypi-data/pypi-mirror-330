import numpy as np
import concurrent.futures
import torch
from typing import List, Dict, Optional
from .utils import normalize_probabilities

class HydraSearch:
    def __init__(self, search_space_size: int, num_searchers: int = 10, threshold_high: float = 0.5, threshold_low: float = 0.3, parallel_mode: str = 'cpu') -> None:
        """
        Hydra Search Algorithm Implementation.
        
        :param search_space_size: Number of sections in the search space.
        :param num_searchers: Initial number of searchers.
        :param threshold_high: Probability threshold for searcher multiplication.
        :param threshold_low: Probability threshold for searcher self-destruction.
        :param parallel_mode: 'cpu' for CPU parallelism, 'gpu' for CUDA acceleration.
        """
        self.search_space_size = search_space_size
        self.num_searchers = num_searchers
        self.threshold_high = threshold_high
        self.threshold_low = threshold_low
        self.parallel_mode = parallel_mode
        self.sections = self._initialize_sections()
        
    def _initialize_sections(self) -> List[Dict[str, float]]:
        """Initialize search space sections with equal probability."""
        probabilities = np.full(self.num_searchers, 1 / self.num_searchers)
        return [{'prob': float(p), 'searchers': 1} for p in probabilities]
    
    def _update_probability(self, section: Dict[str, float]) -> Dict[str, float]:
        """Apply controlled probability updates with numerical stability."""
        noise_factor = np.random.uniform(0.95, 1.05)  # Reduced noise for better control
        section['prob'] *= noise_factor
        return section

    def step(self) -> None:
        """Perform one iteration of Hydra Search with optimized parallel execution."""
        if self.parallel_mode == 'cpu':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                self.sections = list(executor.map(self._update_probability, self.sections))
        elif self.parallel_mode == 'gpu' and torch.cuda.is_available():
            prob_tensor = torch.tensor([s['prob'] for s in self.sections], device='cuda', dtype=torch.float32)
            prob_tensor *= torch.rand(prob_tensor.shape, device='cuda', dtype=torch.float32)
            prob_tensor = normalize_probabilities(prob_tensor.cpu().numpy())
            for i, section in enumerate(self.sections):
                section['prob'] = float(prob_tensor[i])
        
        total_prob = sum(s['prob'] for s in self.sections)
        if total_prob == 0:
            return  # Prevent division by zero
        
        for section in self.sections:
            section['prob'] /= total_prob
        
        # Sort sections in ascending order of probability
        self.sections.sort(key=lambda s: s['prob'])
        
        # Gradually remove the lowest probability section
        if len(self.sections) > 1:
            self.sections.pop(0)  # Remove the weakest section
    
    def run(self, iterations: int = 10) -> Optional[int]:
        """Run the Hydra Search algorithm until only one section remains, then return its index."""
        for _ in range(iterations):
            self.step()
        
        # The last remaining section is the best one
        return 0 if not self.sections else self.sections.index(self.sections[0])
    
# Example Usage
if __name__ == "__main__":
    hsa = HydraSearch(search_space_size=100, num_searchers=10, parallel_mode='cpu')
    best_index = hsa.run(iterations=10)
    if best_index is not None:
        print("Best Section Index:", best_index)
    else:
        print("No valid section found.")
