"""Tests for CLI commands."""
import os
from unittest import TestCase
from qiskit_ibm_runtime import IBMRuntimeService
import pandas as pd
from src.workflow import Workflow


def authentication():
    """Authentication function."""
    QS_TOKEN = os.environ.get("QS_TOKEN")
    if QS_TOKEN is not None:
        Workflow.authentication(auth="legacy", token=QS_TOKEN, overwrite=True)


class TestUtils(TestCase):
    """Test class for Workflow cli."""

    def test_authentication(self):
        """Test for Authentication command."""
        authentication()

        service = IBMRuntimeService()
        self.assertTrue(service.active_account()["verify"], True)

    def test_kernel_flow(self):
        """Test for Kernel flow command."""
        authentication()
        circuits_tpl = [5]
        feather_files = Workflow.kernel_flow(
            circuit_tpl_id=circuits_tpl, matrix_size=[1, 1]
        )

        for circuit, fea_file in zip(circuits_tpl, feather_files):
            self.assertEqual(fea_file, "kernels-" + str(circuit) + "-ideal.csv")

    def test_view_kernel(self):
        """Test to test the view kernel command."""
        data_file = Workflow.view_kernel(file_name="kernels-2-ideal.csv")
        self.assertTrue(isinstance(data_file, pd.DataFrame))
