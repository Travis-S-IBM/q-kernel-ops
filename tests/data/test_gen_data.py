"""Tests for data."""
import sys
from time import time
from typing import List
from unittest import TestCase
from src.data import kernel_metadata, kernel_telemetry, completion_telemetry
from src.controllers import Kernel
from tests.runtime import return_sampler, return_circuit_runner


class TestUtils(TestCase):
    """Test class for data generative functions."""

    def test_kernel_metadata(self):
        """Test to test the kernel metadata function."""
        re_sampler, telemetry_info, _, _ = return_sampler.get_sampler()
        circuits_2 = list(range(901, 901 + int(len(re_sampler["quasi_dists"]) / 2)))
        seed_x_2 = [
            42 for _ in range(int(len(re_sampler["quasi_dists"]) / len(circuits_2)))
        ]
        seed_y_2 = [
            4242 for _ in range(int(len(re_sampler["quasi_dists"]) / len(circuits_2)))
        ]

        fea_files_2 = kernel_metadata(
            circuit_tpl_id=circuits_2,
            job_id=telemetry_info[0],
            width=4,
            seed1=seed_x_2,
            seed2=seed_y_2,
            backend="ibmq_qasm_simulator",
            runtime_result=re_sampler,
        )
        self.assertTrue(isinstance(fea_files_2, List))

        circuits_3 = list(range(901, 901 + int(len(re_sampler["quasi_dists"]) / 3)))
        seed_x_3 = [
            42 for _ in range(int(len(re_sampler["quasi_dists"]) / len(circuits_3)))
        ]
        seed_y_3 = [
            4242 for _ in range(int(len(re_sampler["quasi_dists"]) / len(circuits_3)))
        ]

        fea_files_3 = kernel_metadata(
            circuit_tpl_id=circuits_3,
            job_id=telemetry_info[0],
            width=4,
            seed1=seed_x_3,
            seed2=seed_y_3,
            backend="ibmq_qasm_simulator",
            runtime_result=re_sampler,
        )
        self.assertTrue(isinstance(fea_files_3, List))

        (
            re_statevector,
            telemetry_info,
            _,
            _,
        ) = return_circuit_runner.get_circuit_runner()
        circuits_2 = list(range(901, 901 + int(len(re_statevector["results"]) / 2)))
        seed_x_2 = [
            42 for _ in range(int(len(re_statevector["results"]) / len(circuits_2)))
        ]
        seed_y_2 = [
            4242 for _ in range(int(len(re_statevector["results"]) / len(circuits_2)))
        ]

        fea_files_2 = kernel_metadata(
            circuit_tpl_id=circuits_2,
            job_id=telemetry_info[0],
            width=4,
            seed1=seed_x_2,
            seed2=seed_y_2,
            backend="simulator-statevector",
            runtime_result=re_sampler,
        )
        self.assertTrue(isinstance(fea_files_2, List))

    def test_kernel_telemetry(self):
        """Test to test the kernel telemetry function."""
        kernel_circuits = Kernel(
            circuit_tpl_id=[2],
            width=4,
            layer=1,
            seed_x=[0, 1, 1],
            seed_y=[0, 0, 1],
        )
        kernel_circuits.gen_circuits_tpl()
        # Gen kernel circuits
        kernel_circuits.gen_kernel_circuits()

        _, te_sampler, _, program_id = return_sampler.get_sampler()

        fea_files = kernel_telemetry(
            circuit_tpl_id=kernel_circuits.circuit_tpl_id,
            job_id=te_sampler[0],
            time_queue=float(te_sampler[1]),
            time_simu=float(te_sampler[2]),
            payload_size=sys.getsizeof(kernel_circuits.kernel_cirq),
            width=kernel_circuits.width,
            layer=kernel_circuits.layer,
            shots=kernel_circuits.shots,
            program_id=program_id,
            nb_circuits=6,
            comment=te_sampler[3],
        )
        self.assertTrue(isinstance(fea_files, str))

        _, te_sampler, _, program_id = return_circuit_runner.get_circuit_runner()

        fea_files = kernel_telemetry(
            circuit_tpl_id=kernel_circuits.circuit_tpl_id,
            job_id=te_sampler[0],
            time_queue=float(te_sampler[1]),
            time_simu=float(te_sampler[2]),
            payload_size=sys.getsizeof(kernel_circuits.kernel_cirq),
            width=kernel_circuits.width,
            layer=kernel_circuits.layer,
            shots=kernel_circuits.shots,
            program_id=program_id,
            nb_circuits=6,
            comment=te_sampler[3],
        )
        self.assertTrue(isinstance(fea_files, str))

    def test_completion_telemetry(self):
        """Test to test the completion telemetry function."""

        fea_files = completion_telemetry(
            size_bn=6,
            size_ln=3,
            over_u=1,
            rank=2,
            nb_qubits=2,
            size_np=200,
            pourcent_sparcity=0.03,
            time_cmpl=time(),
            error_mse=0.0003,
            error_norm=0.67,
            comment="SUCCESS",
        )
        self.assertTrue(isinstance(fea_files, str))
