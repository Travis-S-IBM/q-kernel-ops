"""Workflow class for controlling all CLI functions."""

import sys
from typing import List
from qiskit_ibm_runtime import SamplerResult, IBMRuntimeService
from src.circuits import circuit_5, circuit_2, kernel_circuit
from src.runtime import run_sampler


class Workflow:
    """Worflow class.
    Entrypoint for all CLI commands.

    Each public method of this class is CLI command
    and arguments for method are options/flags for this command.

    Ex: `python worflow.py kernel_flow --circuit_tpl_id=[2,5]`
    """

    def __init__(self):
        pass

    @staticmethod
    def authentication(
        auth: str, token: str, instance="ibm-q/open/main", overwrite=False
    ) -> None:
        """Commands for authentication.

        Args:
            auth: if you have a Cloud account : "cloud", is you have an Quantum account "legacy"
            token: your IBM Cloud/Quantum token
            instance: group path for computer access
            overwrite: set True if you want to overwrite your actual token

        Return:
            Register the session in disk space
        """
        IBMRuntimeService.save_account(
            auth=auth, token=token, instance=instance, overwrite=overwrite
        )

    @staticmethod
    def kernel_flow(
        circuit_tpl_id: [int],
        width: int = 4,
        layer: int = 1,
        seed1: int = 42,
        seed2: int = 4242,
        matrix_size: List[int] = None,
        backend: str = "ibmq_qasm_simulator",
        shots: int = 1024,
        verbose: bool = False,
    ) -> SamplerResult:
        """Command for calling body issue parsing function.

        Args:
            circuit_tpl_id: list of circuit id to run as template
            width: number of qubits
            layer: number of reps for the tpl
            seed1: seed for x axes
            seed2: seed for y axes
            matrix_size: matrix size for seed coordinate [x, y]
            backend: backend for running circuit
            shots: number of shots for the circuit
            verbose: print all kind of information

        Returns:
            logs output
            SamplerResult: result of the kernel job
        """

        seed_x = []
        seed_y = []

        if matrix_size is not None:
            if matrix_size[0] != matrix_size[1]:
                print("""
                The coordinate have to be square.
                Ex. [2,2] or [5,5]
                """)
                sys.exit(1)
            for x_axe in range(matrix_size[0] + 1):
                for y_axe in range(matrix_size[1] + 1):
                    seed_x.append(x_axe)
                    seed_y.append(y_axe)
        else:
            seed_x.append(seed1)
            seed_y.append(seed2)

        circuit_tpl = []
        for tpl_id in circuit_tpl_id:
            if tpl_id == 2:
                circuit_tpl.append(circuit_2(width=width, layer=layer, verbose=verbose))
            elif tpl_id == 5:
                circuit_tpl.append(circuit_5(width=width, layer=layer, verbose=verbose))
            else:
                print("Please chooce a circuit_tpl_id between [2, 5, X, X]")
                sys.exit(1)

        kernel_cirq = []
        for tpl in circuit_tpl:
            for index, _ in enumerate(seed_x):
                kernel_cirq.append(
                    kernel_circuit(
                        circuit=tpl,
                        seed1=seed_x[index],
                        seed2=seed_y[index],
                        verbose=verbose,
                    )
                )

        run = run_sampler(
            circuits=kernel_cirq, backend=backend, shots=shots, verbose=verbose
        )

        print(
            "::set-output name={name}::{value}".format(name="KernelResult", value=run)
        )

        return run
