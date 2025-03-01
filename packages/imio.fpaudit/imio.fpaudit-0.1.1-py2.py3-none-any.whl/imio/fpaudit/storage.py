from imio.fpaudit import LOG_DIR
from imio.fpaudit.interfaces import ILogsStorage
from imio.fpaudit.logger import FPAuditLogInfo
from zope.component import getUtility
from zope.interface import implementer

import os


@implementer(ILogsStorage)
class LogsStorageUtility(object):
    """Utility to store logs instances"""

    def __init__(self):
        self.storage = {}

    def add(self, key, value):
        """Add a log entry in storage."""
        self.storage[key] = value

    def set(self, dic):
        """Set storage to dic"""
        self.storage = dic

    def get(self, key, default=None):
        """Get a key from storage"""
        return self.storage.get(key, default)

    def remove(self, key):
        """Remove key from storage"""
        if key in self.storage:
            del self.storage[key]


def store_config(logs_config):
    """Store logs configuration in utility."""
    dic = {}
    for entry in logs_config:
        log_i = FPAuditLogInfo(
            {"audit-log": os.path.join(LOG_DIR, entry["audit_log"])},
            entry["log_id"],
            logformat=entry["log_format"],
        )
        log_i.handler.formatter.datefmt = "%Y-%m-%d %H:%M:%S"
        dic[entry["log_id"]] = log_i
    storage = getUtility(ILogsStorage)
    storage.set(dic)
