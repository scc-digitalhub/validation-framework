"""
Logger module.
"""
import logging

# LOGGER
LOGGER = logging.getLogger("datajudge")
LOGGER.setLevel(logging.INFO)

# create console handler and set level to debug

class LogFilter(logging.Filter):
    """
    Logs filter.
    """
    def filter(self, record):
        """
        Filter for datajudge logs.
        """
        return record.name == "datajudge"

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.addFilter(LogFilter())

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
LOGGER.addHandler(ch)
