"""Workflow class for controlling all CLI functions."""

from qiskit_ibm_runtime import SamplerResult, IBMRuntimeService
from src.circuits import circuit_5, circuit_2, kernel_circuit
from src.runtime import run_sampler
import sys


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
        width=4,
        layer=1,
        seed1=42,
        seed2=4242,
        backend="ibmq_qasm_simulator",
        shots=1024,
        verbose=False,
    ) -> SamplerResult:
        """Command for calling body issue parsing function.

        Args:
            circuit_tpl_id: list of circuit id to run as template
            width: number of qubits
            layer: number of reps for the tpl
            seed1: seed for x axes
            seed2: seed for y axes
            backend: backend for running circuit
            shots: number of shots for the circuit
            verbose: print all kind of information

        Returns:
            logs output
            SamplerResult: result of the kernel job
        """
        circuit_tpl_id = circuit_tpl_id
        width = width
        layer = layer
        seed1 = seed1
        seed2 = seed2
        backend = backend
        shots = shots
        verbose = verbose

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
            kernel_cirq.append(
                kernel_circuit(circuit=tpl, seed1=seed1, seed2=seed2, verbose=verbose)
            )

        run = run_sampler(
            circuits=kernel_cirq, backend=backend, shots=shots, verbose=verbose
        )

        print(
            "::set-output name={name}::{value}".format(name="KernelResult", value=run)
        )

        return run