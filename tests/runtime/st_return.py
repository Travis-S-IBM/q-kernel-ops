"""Generate common need for runtime return."""
from time import time, sleep
from typing import Tuple


def get_time() -> Tuple[float, float]:
    start_time = time()
    sleep(5)
    time_queue = time() - start_time
    sleep(2)
    time_simu = time() - time_queue - start_time

    return time_queue, time_simu


def get_exception() -> str:
    return "None"


def get_standard() -> Tuple[list, str]:
    time_queue, time_simu = get_time()
    tele_comment = "SUCCESS"
    telemetry_info = ["fzgezgrzgz", time_queue, time_simu, tele_comment]
    catch_exception = get_exception()

    return telemetry_info, catch_exception
