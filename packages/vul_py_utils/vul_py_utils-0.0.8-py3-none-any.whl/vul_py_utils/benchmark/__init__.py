"""
    This module is used to benchmark the time of a function. 
    The decorator @benchmark_log will print the time elapsed of the function.
"""
import datetime


def start_tick() -> datetime.datetime:
    """
    Mark the time to start benchmarking
    """
    return datetime.datetime.now()


def elapse(start: datetime.datetime, msg: str = "") -> str:
    """
    Get message timestamp of benchmark
    """
    if msg != "":
        return f"[{start}] " + msg + f": {datetime.datetime.now() - start}"
    return f"[{start}] Total time processing: {datetime.datetime.now() - start}"


def benchmark_log(f):
    """_summary_

    Args:
        f (_type_): _description_
    """
    def wrapper(*args, **kwargs):
        start = start_tick()
        res = f(*args, **kwargs)
        print(f.__name__, elapse(start))
        return res
    return wrapper
