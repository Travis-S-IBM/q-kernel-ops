"""Tests for Kernel commands."""
from unittest import TestCase
from src.runtime import run_sampler
from src.circuits import circuit_2, circuit_5, kernel_circuit
from qiskit_ibm_runtime import SamplerResult
from tests.test_workflow import authentication


class TestUtils(TestCase):
    """Test class for runtime functions."""

    def test_run_sampler(self):
        """Test for run sampler function."""
        authentication()
        kernel_cirq = [kernel_circuit(circuit_2(), 42, 4242)]
        run = run_sampler(circuits=kernel_cirq)
        self.assertTrue(isinstance(run, SamplerResult))
        self.assertEqual(len(kernel_cirq), len(run.quasi_dists))

        kernel_cirq = [
            kernel_circuit(circuit_2(), 42, 4242),
            kernel_circuit(circuit_5(), 24, 2424),
        ]
        run = run_sampler(circuits=kernel_cirq)
        self.assertTrue(isinstance(run, SamplerResult))
        self.assertEqual(len(kernel_cirq), len(run.quasi_dists))
