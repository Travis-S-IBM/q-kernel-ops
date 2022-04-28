"""Tests for CLI commands."""
import os
from unittest import TestCase
from qiskit_ibm_runtime import QiskitRuntimeService
import pandas as pd
from src.workflow import Workflow


def authentication():
    """Authentication function."""
    qs_token = os.environ.get("QS_TOKEN")
    if qs_token is not None:
        Workflow.authentication(channel="ibm_quantum", token=qs_token, overwrite=True)


class TestUtils(TestCase):
    """Test class for Workflow cli."""

    def test_authentication(self):
        """Test for Authentication command."""
        authentication()

        service = QiskitRuntimeService()
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

    def test_view_telemetry(self):
        """Test to test the view telemetry command."""
        data_file = Workflow.view_telemetry()
        self.assertTrue(isinstance(data_file, pd.DataFrame))

    def test_sync_data(self):
        """Test to test the sync data command."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.mkdir("{}/../resources/shared_folder".format(current_dir))
        sync_result = Workflow.sync_data(
            sha_folder="resources/shared_folder", git_sync=False
        )
        self.assertTrue(
            True
            if sync_result == "sync data done !"
            or sync_result == "An error occurred, lockfile unlock."
            else False
        )
