# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.globalrequest.local import setLocal

import imio.fpaudit
import os


class ImioFPAuditLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base layer.
        self.loadZCML(package=imio.fpaudit)

    def setUpPloneSite(self, portal):
        setLocal("request", portal.REQUEST)  # to avoid error with empty request in P6
        applyProfile(portal, "imio.fpaudit:default")
        setRoles(portal, TEST_USER_ID, ["Manager"])


IMIO_FPAUDIT_FIXTURE = ImioFPAuditLayer()


IMIO_FPAUDIT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIO_FPAUDIT_FIXTURE,), name="ImioFPAuditLayer:IntegrationTesting"
)


IMIO_FPAUDIT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IMIO_FPAUDIT_FIXTURE,), name="ImioFPAuditLayer:FunctionalTesting"
)


def write_temp_files(temp_dir, filenames):
    for filename in filenames:
        with open(os.path.join(temp_dir, filename), "w") as f:
            f.write("test")


def clear_temp_dir(temp_dir):
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
