import time
from functools import wraps
from pyutile.reporting.logged import logger as log

def log_execution_time(func):
    """Decorator to log the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        log.info(f"Function '{func.__name__}' executed in {elapsed:.4f} seconds.")
        return result
    return wrapper
