"""
#############################################
#
# kernel.py
#
# function for kernel programs
#
#
#############################################
"""

import sys

from src.circuits import circuit_2, circuit_5, circuit_10, circuit_18, kernel_circuit
from src.data import kernel_metadata, kernel_telemetry
from src.runtime import run_runtime


def gen_circuits_tpl(
    circuit_tpl_id: [int], width: int = 4, layer: int = 1, verbose: bool = False
) -> list:
    """Function to gen template circuits.

    Args:
        circuit_tpl_id: list of circuit id to run as template
        width: number of qubits
        layer: number of reps for the tpl
        verbose: print all kind of information
    Returns:
        List of template quantum circuits
    """
    circuits_tpl = []
    for tpl_id in circuit_tpl_id:
        if tpl_id == 2:
            circuits_tpl.append(circuit_2(width=width, layer=layer, verbose=verbose))
        elif tpl_id == 5:
            circuits_tpl.append(circuit_5(width=width, layer=layer, verbose=verbose))
        elif tpl_id == 10:
            circuits_tpl.append(circuit_10(width=width, layer=layer, verbose=verbose))
        elif tpl_id == 18:
            circuits_tpl.append(circuit_18(width=width, layer=layer, verbose=verbose))
        else:
            print("Please chooce a circuit_tpl_id between [2, 5, 10, 18, X]")
            sys.exit(1)

    return circuits_tpl


def gen_kernel_circuits(
    circuits_tpl: list, seed_x: [int], seed_y: [int], verbose: bool = False
) -> list:
    """Function to generate the kernel circuits.

    Args:
        circuits_tpl: list of template quantum circuits
        seed_x: seed for x axes
        seed_y: seed for y axes
        verbose: print all kind of information
    Return:
        list of kernel circuits
    """
    kernel_cirq = []
    for tpl in circuits_tpl:
        for index, _ in enumerate(seed_x):
            kernel_cirq.append(
                kernel_circuit(
                    circuit=tpl,
                    seed1=seed_x[index],
                    seed2=seed_y[index],
                    verbose=verbose,
                )
            )
    return kernel_cirq


def kernel_endpoint(
    circuit_tpl_id: [int],
    seed_x: [int],
    seed_y: [int],
    width: int = 4,
    layer: int = 1,
    backend: str = "ibmq_qasm_simulator",
    shots: int = 1024,
    verbose: bool = False,
) -> [str]:
    """Command for kernel matrix generation.

    Args:
        circuit_tpl_id: list of circuit id to run as template
        width: number of qubits
        layer: number of reps for the tpl
        seed_x: seed for x axes
        seed_y: seed for y axes
        backend: backend for running circuit
        shots: number of shots for the circuit
        verbose: print all kind of information

    Returns:
        logs output
        Array of data files name
    """
    circuits_tpl = gen_circuits_tpl(
        circuit_tpl_id=circuit_tpl_id, width=width, layer=layer, verbose=verbose
    )

    kernel_cirq = gen_kernel_circuits(
        circuits_tpl=circuits_tpl, seed_x=seed_x, seed_y=seed_y, verbose=verbose
    )

    run, telemetry_info, catch_exception, program_id = run_runtime(
        circuits=kernel_cirq, backend=backend, shots=shots, verbose=verbose
    )

    kernel_telemetry(
        circuit_tpl_id=circuit_tpl_id,
        job_id=telemetry_info[0],
        time_queue=float(telemetry_info[1]),
        time_simu=float(telemetry_info[2]),
        payload_size=sys.getsizeof(kernel_cirq),
        width=width,
        layer=layer,
        shots=shots,
        program_id=program_id,
        nb_circuits=len(kernel_cirq),
        comment=telemetry_info[3],
    )

    if catch_exception == "None":

        return_str = kernel_metadata(
            circuit_tpl_id=circuit_tpl_id,
            job_id=telemetry_info[0],
            width=width,
            seed1=seed_x,
            seed2=seed_y,
            backend=backend,
            runtime_result=run,
        )

    else:
        if telemetry_info[3] == "Unknown Error":
            return_str = (
                "Telemetry complete but Runtime failed ! "
                + telemetry_info[3]
                + " \nException::"
                + catch_exception
            )
        else:
            return_str = "Telemetry complete but Runtime failed ! " + telemetry_info[3]

    return return_str
