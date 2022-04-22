"""Generate circuit-runner return."""
from ast import literal_eval
from time import time, sleep
from typing import Tuple


def get_circuit_runner() -> Tuple[dict, list, str]:
    """Function to get a sample of SamplerResult object."""
    run = {
        "results": [
            literal_eval(
                "{'header': { 'global_phase': 6.2831853071795845, 'name': 'circuit-553' } }"
            ),
            literal_eval(
                "{'header': { 'global_phase': 0.7112925677954506, 'name': 'circuit-554' } }"
            ),
            literal_eval(
                "{'header': { 'global_phase': 6.2831853071795845, 'name': 'circuit-545' } }"
            ),
            literal_eval(
                "{'header': { 'global_phase': 3.2831851871795845, 'name': 'circuit-556' } }"
            ),
            literal_eval(
                "{'header': { 'global_phase': 5.2831853071198045, 'name': 'circuit-557' } }"
            ),
            literal_eval(
                "{'header': { 'global_phase': 4.2831853071795845, 'name': 'circuit-558' } }"
            ),
        ],
        "metadata": {
            "time_taken": 0.000944715,
            "time_taken_execute": 0.000240511,
        },
    }
    start_time = time()
    sleep(5)
    time_queue = time() - start_time
    sleep(2)
    time_simu = time() - time_queue - start_time
    tele_comment = "SUCCESS"
    telemetry_info = ["fzgezgrzgz", time_queue, time_simu, tele_comment]
    catch_exception = "None"
    return run, telemetry_info, catch_exception
