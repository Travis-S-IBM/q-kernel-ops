"""Tests for data."""
import sys
from typing import List
from unittest import TestCase
from src.data import kernel_metadata, kernel_telemetry
from src.controllers import gen_kernel_circuits, gen_circuits_tpl
from tests.runtime import return_sampler


class TestUtils(TestCase):
    """Test class for data generative functions."""

    def test_kernel_metadata(self):
        """Test to test the kernel metadata function."""
        re_sampler, _ = return_sampler.get_sampler()
        circuits_2 = list(range(901, 901 + int(len(re_sampler["quasi_dists"]) / 2)))
        seed_x_2 = [
            42 for _ in range(int(len(re_sampler["quasi_dists"]) / len(circuits_2)))
        ]
        seed_y_2 = [
            4242 for _ in range(int(len(re_sampler["quasi_dists"]) / len(circuits_2)))
        ]

        fea_files_2 = kernel_metadata(
            circuit_tpl_id=circuits_2,
            width=4,
            layer=3,
            shots=1024,
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
            width=4,
            layer=3,
            shots=1024,
            seed1=seed_x_3,
            seed2=seed_y_3,
            backend="ibmq_qasm_simulator",
            runtime_result=re_sampler,
        )
        self.assertTrue(isinstance(fea_files_3, List))

    def test_kernel_telemetry(self):
        """Test to test the kernel telemetry function."""
        circuits_tpl = gen_circuits_tpl(circuit_tpl_id=[2], width=4, layer=1)
        kernel_cirq = gen_kernel_circuits(
            circuits_tpl=circuits_tpl, seed_x=[0, 1, 1], seed_y=[0, 0, 1]
        )

        _, te_sampler = return_sampler.get_sampler()

        print("Tele : ", te_sampler)

        fea_files = kernel_telemetry(
            circuit_tpl_id=[2],
            job_id=te_sampler[0],
            time_queue=float(te_sampler[1]),
            time_simu=float(te_sampler[2]),
            payload_size=sys.getsizeof(kernel_cirq),
            width=4,
            layer=1,
            nb_circuits=6,
            comment="SUCCEED",
        )
        self.assertTrue(isinstance(fea_files, str))
