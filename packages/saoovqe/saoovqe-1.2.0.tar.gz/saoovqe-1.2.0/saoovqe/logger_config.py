"""Module containing global settings for logging."""

import logging

log = logging.getLogger("SAOOVQE.logger")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)

log.setLevel(logging.INFO)

log.debug("Logger was configured.")
