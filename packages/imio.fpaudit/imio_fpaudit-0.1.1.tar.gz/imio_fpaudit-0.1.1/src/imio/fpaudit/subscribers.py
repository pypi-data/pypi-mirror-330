# -*- coding: utf-8 -*-
from imio.fpaudit.storage import store_config
from imio.helpers.security import get_zope_root
from imio.helpers.security import set_site_from_package_config
from plone import api

import os
import transaction


def zope_ready(event):
    """Not going here in test"""
    zope_app = get_zope_root()
    site = set_site_from_package_config("imio.fpaudit", zope_app=zope_app)
    change = False
    if site:
        if os.getenv("INSTANCE_HOME", "").endswith("/instance1") or os.getenv("INSTANCE_HOME", "").endswith(
            "/instance"
        ):
            with api.env.adopt_user("admin"):
                log_entries = api.portal.get_registry_record("imio.fpaudit.settings.log_entries", default=[])
                if log_entries:
                    store_config(log_entries)
                    change = True
    if change:
        transaction.commit()
