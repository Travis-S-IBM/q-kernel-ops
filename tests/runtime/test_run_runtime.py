"""Tests for Kernel commands."""
from unittest import TestCase
from src.runtime import run_runtime
from src.circuits import circuit_2, circuit_5, kernel_circuit
from tests.test_workflow import authentication


class TestUtils(TestCase):
    """Test class for runtime functions."""

    def test_run_runtime(self):
        """Test for run sampler function."""
        authentication()
        kernel_cirq = [kernel_circuit(circuit_2(), 42, 4242)]
        run, telemetry_info, catch_exception = run_runtime(circuits=kernel_cirq)
        self.assertTrue(isinstance(run, dict))
        self.assertEqual(len(kernel_cirq), len(run["quasi_dists"]))
        self.assertTrue(list(telemetry_info))
        self.assertEqual(len(telemetry_info), 4)
        self.assertEqual(catch_exception, "None")

        kernel_cirq = [
            kernel_circuit(circuit_2(), 42, 4242),
            kernel_circuit(circuit_5(), 24, 2424),
        ]
        run, telemetry_info, catch_exception = run_runtime(circuits=kernel_cirq)
        self.assertTrue(isinstance(run, dict))
        self.assertEqual(len(kernel_cirq), len(run["quasi_dists"]))
        self.assertTrue(list(telemetry_info))
        self.assertEqual(len(telemetry_info), 4)
        self.assertEqual(catch_exception, "None")

        run, telemetry_info, catch_exception = run_runtime(
            circuits=kernel_cirq, backend="simulator_statevector"
        )
        self.assertTrue(isinstance(run, dict))
        self.assertEqual(len(kernel_cirq), len(run["results"]))
        self.assertTrue(list(telemetry_info))
        self.assertEqual(len(telemetry_info), 4)
        self.assertEqual(catch_exception, "None")
