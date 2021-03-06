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

import os
import pandas as pd


def kernel_metadata(
    circuit_tpl_id: [int],
    job_id: [str],
    width: int,
    seed1: [int],
    seed2: [int],
    backend: str,
    runtime_result: dict,
) -> [str]:
    """Function generate kernel metadata files.

    Args:
        circuit_tpl_id: list of circuit id to run as template
        job_id: array of ids of the experiments
        width: number of qubits
        seed1: seed for x axes
        seed2: seed for y axes
        backend: backend used for the experiment
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

        if backend == "simulator_statevector":
            min_lim = int(
                circ_index * len(runtime_result["results"]) / len(circuit_tpl_id)
            )
            max_lim = int(
                len(runtime_result["results"]) / len(circuit_tpl_id) + min_lim
            )
            for i in range(min_lim, max_lim):
                fidelity.append(runtime_result["results"][i]["header"]["global_phase"])

        else:
            min_lim = int(
                circ_index * len(runtime_result["quasi_dists"]) / len(circuit_tpl_id)
            )
            max_lim = int(
                len(runtime_result["quasi_dists"]) / len(circuit_tpl_id) + min_lim
            )
            for i in range(min_lim, max_lim):
                if runtime_result["quasi_dists"][i].get(wanted_result) is not None:
                    fidelity.append(runtime_result["quasi_dists"][i][wanted_result])
                elif runtime_result["quasi_dists"][i].get("0") is not None:
                    fidelity.append(runtime_result["quasi_dists"][i]["0"])
                else:
                    fidelity.append(0)

        fea_file = {
            "job_id": str(job_id),
            "seed_x": seed1,
            "seed_y": seed2,
            "fidelity": fidelity,
        }
        data_fea = pd.DataFrame(fea_file)

        data_name = "kernels-" + str(circuit) + "-ideal.csv"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dest = "../../resources/kernel_metadata/" + backend
        if not os.path.isdir("{}/{}/".format(current_dir, dest)):
            os.mkdir("{}/{}/".format(current_dir, dest))

        data_fea.to_feather("{}/{}/".format(current_dir, dest) + data_name)

        files.append(backend + "/" + data_name)

    return files
