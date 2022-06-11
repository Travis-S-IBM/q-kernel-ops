"""Tests for Kernel commands."""
from unittest import TestCase
from src.controllers import kernel_endpoint, gen_circuits_tpl, gen_kernel_circuits
from tests.test_workflow import authentication


class TestUtils(TestCase):
    """Test class for kernel endpoint."""

    def test_kernel_endpoint(self):
        """Test for kernel endpoint function."""
        authentication()
        circuits_tpl = [5, 2]
        backend = "ibmq_qasm_simulator"
        feather_files = kernel_endpoint(
            circuit_tpl_id=circuits_tpl, seed_x=[42], seed_y=[4242], backend=backend
        )

        for circuit, fea_file in zip(circuits_tpl, feather_files):
            self.assertEqual(
                fea_file, backend + "/kernels-" + str(circuit) + "-ideal.csv"
            )

    def test_gen_kernel_components(self):
        """Test for gen circuits template & gen kernel circuits function."""
        circuits_tpl_id = [5, 2]
        circuits_tpl = gen_circuits_tpl(circuit_tpl_id=circuits_tpl_id)
        self.assertEqual(len(circuits_tpl), len(circuits_tpl_id))

        seed_x = [42, 24]
        seed_y = [4242, 2424]
        self.assertEqual(len(seed_x), len(seed_y))

        kernel_cirq = gen_kernel_circuits(
            circuits_tpl=circuits_tpl, seed_x=seed_x, seed_y=seed_y
        )
        self.assertEqual(len(kernel_cirq), len(seed_x) * len(circuits_tpl))
        self.assertEqual(len(kernel_cirq), len(seed_y) * len(circuits_tpl))
