"""Tests for Kernel commands."""
from unittest import TestCase, skip
from q_kernel_ops.runtime import Runtime
from q_kernel_ops.circuits import circuit_2, circuit_5, kernel_circuit
from tests.test_workflow import authentication


class TestUtils(TestCase):
    """Test class for runtime functions."""

    @skip("Remote call.")
    def test_run_runtime(self):
        """Test for run sampler function."""
        authentication()
        kernel_cirq = [kernel_circuit(circuit_2(), 42, 4242)]
        run = Runtime()
        run.run_runtime(circuits=kernel_cirq)
        self.assertTrue(isinstance(run.result, dict))
        self.assertEqual(len(kernel_cirq), len(run.result["quasi_dists"]))
        self.assertEqual(run.catch_exception, None)
        self.assertEqual(run.program_id, "sampler")

        kernel_cirq = [
            kernel_circuit(circuit_2(), 42, 4242),
            kernel_circuit(circuit_5(), 24, 2424),
        ]
        run = Runtime()
        run.run_runtime(circuits=kernel_cirq)
        self.assertTrue(isinstance(run.result, dict))
        self.assertEqual(len(kernel_cirq), len(run.result["quasi_dists"]))
        self.assertEqual(run.catch_exception, None)
        self.assertEqual(run.program_id, "sampler")

        run = Runtime()
        run.run_runtime(circuits=kernel_cirq, backend="simulator_statevector")
        self.assertTrue(isinstance(run.result, dict))
        self.assertEqual(len(kernel_cirq), len(run.result["results"]))
        self.assertEqual(run.catch_exception, None)
        self.assertEqual(run.program_id, "circuit-runner")
