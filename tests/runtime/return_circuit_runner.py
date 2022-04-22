"""Generate circuit-runner return."""
from ast import literal_eval
from typing import Tuple
from .st_return import get_standard


def get_circuit_runner() -> Tuple[dict, list, str, str]:
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
    telemetry_info, catch_exception = get_standard()
    program_id = "circuit-runner"
    return run, telemetry_info, catch_exception, program_id
