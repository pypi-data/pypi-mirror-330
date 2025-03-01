# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IImioFPAuditLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ILogsStorage(Interface):
    """Logs storage utility interface"""

    def add(key, value):
        """Add a log entry in storage"""

    def set(key, dic):
        """Set storage to dic"""

    def get(key, default=None):
        """Get a key from storage"""

    def remove(key):
        """Remove key from storage"""
