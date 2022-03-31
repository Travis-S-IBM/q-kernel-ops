import sys
from typing import List

from src.circuits import circuit_2, circuit_5, circuit_10, circuit_18, kernel_circuit
from src.data import kernel_metadata
from src.runtime import run_sampler


def kernel_endpoint(
    circuit_tpl_id: [int],
    width: int = 4,
    layer: int = 1,
    seed1: int = 42,
    seed2: int = 4242,
    matrix_size: List[int] = None,
    backend: str = "ibmq_qasm_simulator",
    shots: int = 1024,
    verbose: bool = False,
) -> [str]:
    """Command for kernel matrix generation.

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
        Array of data files name
    """

    seed_x = []
    seed_y = []

    if matrix_size is not None:
        if matrix_size[0] != matrix_size[1]:
            print(
                """
            The coordinate have to be square.
            Ex. [2,2] or [5,5]
            """
            )
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
        elif tpl_id == 10:
            circuit_tpl.append(circuit_10(width=width, layer=layer, verbose=verbose))
        elif tpl_id == 18:
            circuit_tpl.append(circuit_18(width=width, layer=layer, verbose=verbose))
        else:
            print("Please chooce a circuit_tpl_id between [2, 5, 10, 18, X]")
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

    if verbose:
        print(
            "::set-output name={name}::{value}".format(name="KernelResult", value=run)
        )

    fea_files = kernel_metadata(
        circuit_tpl_id=circuit_tpl_id,
        width=width,
        layer=layer,
        shots=shots,
        seed1=seed_x,
        seed2=seed_y,
        runtime_result=run,
    )

    return fea_files
