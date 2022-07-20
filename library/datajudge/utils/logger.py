"""
Custom logging module.
"""
import logging

# LOGGER
LOGGER = logging.getLogger("datajudge")
LOGGER.setLevel(logging.INFO)

# create console handler and set level to debug

class LogFilter(logging.Filter):
    def filter(self, record):
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
