"""
#############################################
#
# gen_telemetry.py
#
# program to generate telemetry
#
#
#############################################
"""

import os
import pandas as pd


def kernel_telemetry(
    circuit_tpl_id: [int],
    job_id: str,
    time_queue: float,
    time_simu: float,
    payload_size: int,
    width: int,
    layer: int,
    shots: int,
    program_id: str,
    nb_circuits: int,
    comment: str,
) -> str:
    """Function generate telemetry metadata files.

    Args:
        circuit_tpl_id: list of circuit id to run as template
        job_id: id of the experiment
        time_queue: time stuck in the queue
        time_simu: duration of running everything
        payload_size: size of the payload send into the Runtime
        width: number of qubits
        layer: number of reps for the tpl
        shots: number of shots of the experiments
        program_id: id of the program used
        nb_circuits: number of circuits in the payload
        comment: status of the Runtime, can be SUCCESS or error with why

    Returns:
        Telemetry file name
    """
    data_name = "telemetry_info.csv"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dest = "../../resources/kernel_metadata"
    if os.path.exists("{}/{}/{}".format(current_dir, dest, data_name)):
        old_file = pd.read_feather("{}/{}/{}".format(current_dir, dest, data_name))

        list_width = old_file["width"].tolist()
        list_width.append(width)
        list_layers = old_file["layers"].tolist()
        list_layers.append(layer)
        list_shots = old_file["shots"].tolist()
        list_shots.append(shots)
        list_program_id = old_file["program"].tolist()
        list_program_id.append(program_id)
        list_circuit_id = old_file["circuit_id"].tolist()
        list_circuit_id.append(str(circuit_tpl_id))
        list_job_id = old_file["job_id"].tolist()
        list_job_id.append(job_id)
        list_time_queue = old_file["time_queue"].tolist()
        list_time_queue.append(time_queue)
        list_time_simu = old_file["time_simu"].tolist()
        list_time_simu.append(time_simu)
        list_payload_size = old_file["payload_size"].tolist()
        list_payload_size.append(payload_size)
        list_nb_circuits = old_file["nb_circuits"].tolist()
        list_nb_circuits.append(nb_circuits)
        list_comment = old_file["comment"].tolist()
        list_comment.append(comment)
    else:
        list_width = [width]
        list_layers = [layer]
        list_circuit_id = [str(circuit_tpl_id)]
        list_job_id = [job_id]
        list_shots = [shots]
        list_program_id = [program_id]
        list_time_queue = [time_queue]
        list_time_simu = [time_simu]
        list_payload_size = [payload_size]
        list_nb_circuits = [nb_circuits]
        list_comment = [comment]

    fea_file = {
        "job_id": list_job_id,
        "width": list_width,
        "layers": list_layers,
        "circuit_id": list_circuit_id,
        "shots": list_shots,
        "program": list_program_id,
        "time_queue": list_time_queue,
        "time_simu": list_time_simu,
        "payload_size": list_payload_size,
        "nb_circuits": list_nb_circuits,
        "comment": list_comment,
    }

    data_fea = pd.DataFrame(fea_file)

    data_fea.to_feather("{}/{}/".format(current_dir, dest) + data_name)

    return data_name
