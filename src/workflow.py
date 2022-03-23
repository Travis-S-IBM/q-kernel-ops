"""Workflow class for controlling all CLI functions."""

from src.circuits import circuit_5, circuit_2, kernel_circuit
from qiskit_ibm_runtime import SamplerResult
from src.runtime import run_sampler


class Workflow:
    """Worflow class.
    Entrypoint for all CLI commands.

    Each public method of this class is CLI command
    and arguments for method are options/flags for this command.

    Ex: `python worflow.py kernel_flow --circuit_tpl_id=[2,5] --auth="cloud" --token="very_long_string"`
    """

    def __init__(self):
        pass

    @staticmethod
    def kernel_flow(
        circuit_tpl_id: [int],
        auth: str,
        token: str,
        width=4,
        layer=1,
        seed1=42,
        seed2=4242,
        shots=1024,
        verbose=False,
    ) -> SamplerResult:
        """Command for calling body issue parsing function.

        Args:
            circuit_tpl_id: list of circuit id to run as template
            token: your IBM Cloud/Quantum token
            auth: if you have a Cloud account : "cloud", is you have an Quantum account "legacy"
            width: number of qubits
            layer: number of reps for the tpl
            seed1: seed for x axes
            seed2: seed for y axes
            shots: number of shots for the circuit
            verbose: print all kind of information

        Returns:
            logs output
            SamplerResult: result of the kernel job
        """
        token = token
        auth = auth
        seed1 = seed1
        seed2 = seed2
        shots = shots
        verbose = verbose

        circuit_tpl = []
        for id in circuit_tpl_id:
            # if circuit_tpl_id == 2:
            # circuit_tpl.append(circuit_2(width=width, layer=layer, verbose=verbose))
            if id == 5:
                circuit_tpl.append(circuit_5(width=width, layer=layer, verbose=verbose))
            else:
                print("Please chooce a circuit_tpl_id between [2, 5, X, X]")
                return exit(1)

        kernel_cirq = []
        for tpl in circuit_tpl:
            kernel_cirq.append(
                kernel_circuit(circuit=tpl, seed1=seed1, seed2=seed2, verbose=verbose)
            )

        run = run_sampler(
            circuits=kernel_cirq, auth=auth, token=token, shots=shots, verbose=verbose
        )

        print(
            "::set-output name={name}::{value}".format(name="KernelResult", value=run)
        )

        return run
