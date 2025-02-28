import unittest
import numpy as np
import torch
from hydra_search.core import HydraSearch

class TestHydraSearch(unittest.TestCase):
    def setUp(self):
        self.hsa_cpu = HydraSearch(search_space_size=100, num_searchers=10, parallel_mode='cpu')
        if torch.cuda.is_available():
            self.hsa_gpu = HydraSearch(search_space_size=100, num_searchers=10, parallel_mode='gpu')
        else:
            self.hsa_gpu = None

    def test_initialization(self):
        self.assertEqual(len(self.hsa_cpu.sections), 10)
        self.assertAlmostEqual(sum(s['prob'] for s in self.hsa_cpu.sections), 1.0, places=5)

    def test_step_cpu(self):
        prev_sections = self.hsa_cpu.sections.copy()
        self.hsa_cpu.step()
        self.assertNotEqual(prev_sections, self.hsa_cpu.sections)

    def test_step_gpu(self):
        if self.hsa_gpu:
            prev_sections = self.hsa_gpu.sections.copy()
            self.hsa_gpu.step()
            self.assertNotEqual(prev_sections, self.hsa_gpu.sections)

    def test_run_cpu(self):
        best_section = self.hsa_cpu.run(iterations=10)
        self.assertIsNotNone(best_section)
        self.assertGreaterEqual(best_section['prob'], self.hsa_cpu.threshold_low)

    def test_run_gpu(self):
        if self.hsa_gpu:
            best_section = self.hsa_gpu.run(iterations=10)
            self.assertIsNotNone(best_section)
            self.assertGreaterEqual(best_section['prob'], self.hsa_gpu.threshold_low)

if __name__ == "__main__":
    unittest.main()
