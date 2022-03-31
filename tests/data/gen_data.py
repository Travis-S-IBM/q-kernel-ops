"""Tests for data."""
from typing import List
from unittest import TestCase
from src.data import kernel_metadata
from tests.runtime import return_sampler


class TestUtils(TestCase):
    """Test class for data generative functions."""

    def test_kernel_metadata(self):
        """Test to test the kernel metadata function."""
        re_sampler = return_sampler.get_sampler()
        circuits_2 = list(range(901, 901 + int(len(re_sampler.quasi_dists) / 2)))
        seed_x_2 = [
            42 for i in range(int(len(re_sampler.quasi_dists) / len(circuits_2)))
        ]
        seed_y_2 = [
            4242 for i in range(int(len(re_sampler.quasi_dists) / len(circuits_2)))
        ]

        fea_files_2 = kernel_metadata(
            circuit_tpl_id=circuits_2,
            width=4,
            layer=3,
            shots=1024,
            seed1=seed_x_2,
            seed2=seed_y_2,
            runtime_result=re_sampler,
        )
        self.assertTrue(isinstance(fea_files_2, List))

        circuits_3 = list(range(901, 901 + int(len(re_sampler.quasi_dists) / 3)))
        seed_x_3 = [
            42 for i in range(int(len(re_sampler.quasi_dists) / len(circuits_3)))
        ]
        seed_y_3 = [
            4242 for i in range(int(len(re_sampler.quasi_dists) / len(circuits_3)))
        ]

        fea_files_3 = kernel_metadata(
            circuit_tpl_id=circuits_3,
            width=4,
            layer=3,
            shots=1024,
            seed1=seed_x_3,
            seed2=seed_y_3,
            runtime_result=re_sampler,
        )
        self.assertTrue(isinstance(fea_files_3, List))
