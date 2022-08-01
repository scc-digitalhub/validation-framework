"""
Logger module.
"""
import logging

# LOGGER
LOGGER = logging.getLogger("datajudge")
LOGGER.setLevel(logging.INFO)


# Create console handler set level to INFO and add filter
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

# Create formatter and add to console handler
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add console handler to logger
LOGGER.addHandler(ch)
