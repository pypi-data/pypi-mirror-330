from collective.fingerpointing.config import LOG_FORMAT
from collective.fingerpointing.logger import LogInfo

import logging


class FPAuditLogInfo(LogInfo):
    def __init__(self, config, log_id, logformat=LOG_FORMAT):  # noqa
        self.logger = logging.getLogger("fpa_{}".format(log_id))
        self.logfile = None
        self.handler = None
        self.configure(config, logformat=logformat)
