import numpy as np
import concurrent.futures
import torch
from typing import List, Dict, Optional
from .utils import normalize_probabilities

class HydraSearch:
    def __init__(self, search_space_size: int, num_searchers: int = 10, threshold_high: float = 0.5, threshold_low: float = 0.3, parallel_mode: str = 'cpu') -> None:
        self.search_space_size = search_space_size
        self.num_searchers = num_searchers
        self.threshold_high = threshold_high
        self.threshold_low = threshold_low
        self.parallel_mode = parallel_mode
        self.sections = self._initialize_sections()
        
    def _initialize_sections(self) -> List[Dict[str, float]]:
        probabilities = np.full(self.num_searchers, 1 / self.num_searchers)
        return [{'prob': float(p), 'searchers': 1} for p in probabilities]

    def _update_probability(self, section: Dict[str, float]) -> Dict[str, float]:
        section['prob'] *= np.random.uniform(0.9, 1.1)
        return section

    def step(self) -> None:
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
        for section in self.sections:
            section['prob'] /= total_prob

        new_sections = []
        for section in self.sections:
            if section['prob'] > self.threshold_high:
                section['searchers'] *= 2
            elif section['prob'] < self.threshold_low:
                section['searchers'] = 0
            if section['searchers'] > 0:
                new_sections.append(section)

        self.sections = new_sections

    def run(self, iterations: int = 10) -> Optional[Dict[str, float]]:
        for _ in range(iterations):
            self.step()
        return max(self.sections, key=lambda s: s['prob'], default=None)
