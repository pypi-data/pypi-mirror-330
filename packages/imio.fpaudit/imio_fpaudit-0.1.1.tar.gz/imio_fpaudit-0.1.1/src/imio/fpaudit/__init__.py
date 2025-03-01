# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import os


_ = MessageFactory("imio.fpaudit")

if os.environ.get("ZOPE_HOME", ""):
    BLDT_DIR = "/".join(os.getenv("INSTANCE_HOME", "").split("/")[:-2])
else:  # test env
    BLDT_DIR = os.getenv("PWD", "")

LOG_DIR = BLDT_DIR
if os.path.exists(os.path.join(BLDT_DIR, "var/log")):
    LOG_DIR = os.path.join(BLDT_DIR, "var/log")
