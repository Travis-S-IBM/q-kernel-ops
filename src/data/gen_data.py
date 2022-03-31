"""
#############################################
#
# gen_data.py
#
# program to generate data
#
#
#############################################
"""

from qiskit_ibm_runtime import SamplerResult
import os
import pandas as pd


def kernel_metadata(
    circuit_tpl_id: [int],
    width: int,
    layer: int,
    shots: int,
    seed1: [int],
    seed2: [int],
    runtime_result: SamplerResult,
) -> [str]:
    """Function generate kernel metadata files.

    Args:
        circuit_tpl_id: list of circuit id to run as template
        width: number of qubits
        layer: number of reps for the tpl
        shots: number of shots for the circuit
        seed1: seed for x axes
        seed2: seed for y axes
        runtime_result: result for runtime

    Returns:
        Array of data files name
    """
    files = []
    wanted_result = ""

    for i in range(width):
        wanted_result = wanted_result + "0"

    for circ_index, circuit in enumerate(circuit_tpl_id):
        fidelity = []
        min_lim = int(
            circ_index * len(runtime_result.quasi_dists) / len(circuit_tpl_id)
        )
        max_lim = int(len(runtime_result.quasi_dists) / len(circuit_tpl_id) + min_lim)
        for i in range(min_lim, max_lim):
            if runtime_result.quasi_dists[i].get(wanted_result) is None:
                fidelity.append(0)
            else:
                fidelity.append(runtime_result.quasi_dists[i][wanted_result])

        fea_file = {
            "width": width,
            "layers": layer,
            "shots": shots,
            "seed_x": seed1,
            "seed_y": seed2,
            "fidelity": fidelity,
        }
        df = pd.DataFrame(fea_file)

        data_name = "kernels-" + str(circuit) + "-ideal.csv"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dest = "../../resources/kernel_metadata"
        df.to_feather("{}/{}/".format(current_dir, dest) + data_name)

        files.append(data_name)

    return files