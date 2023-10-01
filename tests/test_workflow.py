"""Tests for CLI commands."""
import os
from unittest import TestCase, skip
from qiskit_ibm_runtime import QiskitRuntimeService
import pandas as pd
from cvxopt import matrix
from q_kernel_ops.workflow import Workflow


def authentication():
    """Authentication function."""
    qs_token = os.environ.get("QS_TOKEN")
    if qs_token is not None:
        Workflow.authentication(channel="ibm_quantum", token=qs_token, overwrite=True)


class TestUtils(TestCase):
    """Test class for Workflow cli."""

    @skip("Remote call.")
    def test_authentication(self):
        """Test for Authentication command."""
        authentication()

        service = QiskitRuntimeService()
        self.assertTrue(service.active_account()["verify"], True)

    @skip("Remote call.")
    def test_kernel_flow(self):
        """Test for Kernel flow command."""
        authentication()
        circuits_tpl = [5]
        backend = "ibmq_qasm_simulator"
        feather_files = Workflow.kernel_flow(
            circuit_tpl_id=circuits_tpl, matrix_size=[1, 1], backend=backend
        )

        for circuit, fea_file in zip(circuits_tpl, feather_files):
            self.assertEqual(
                fea_file, backend + "/kernels-" + str(circuit) + "-ideal.csv"
            )

    def test_view_kernel(self):
        """Test to test the view kernel command."""
        data_file = Workflow.view_kernel(file_name="kernels-2-ideal.csv")
        self.assertTrue(isinstance(data_file, pd.DataFrame))

    def test_completion_flow(self):
        """Test for Completion flow command."""
        file_name = "kernels-2-ideal.csv"
        backend = "ibmq_qasm_simulator"
        numpy_files = Workflow.completion_flow(
            file_name=file_name, nb_qubits=3, backend=backend
        )

        self.assertEqual(numpy_files, backend + "/cmpl_" + file_name + ".npy")

    def test_view_matrix(self):
        """Test to test the view matrix command."""
        data_file = Workflow.view_matrix(file_name="cmpl_kernels-2-ideal.csv.npy")
        self.assertTrue(isinstance(data_file, matrix))

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
            bool(
                sync_result
                in (
                    "sync data done ! - kernel metadata - telemetry data",
                    "An error occurred, lockfile unlock.",
                )
            )
        )
