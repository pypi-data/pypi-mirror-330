from pyutile.reporting.logged import log, log_manager
from pyutile.reporting.metrics import log_execution_time

# Log messages at various levels.
log.debug("Debugging information")
log.info("Application started")
log.warning("Potential issue detected")
log.error("An error occurred!")
log.critical("Critical failure!")

# Dynamically change the log level at runtime.
log_manager.set_log_level("WARNING")
log.info("This INFO log will now be filtered out.")

# Example of tracking function execution time.
@log_execution_time
def compute():
    total = 0
    for i in range(1000000):
        total += i
    return total

result = compute()

