from imio.fpaudit.browser.settings import IFPAuditSettings
from imio.fpaudit.interfaces import ILogsStorage
from imio.fpaudit.logger import FPAuditLogInfo
from imio.fpaudit.testing import IMIO_FPAUDIT_INTEGRATION_TESTING
from plone import api
from z3c.form import validator
from zope.component import getUtility
from zope.interface import Invalid

import unittest


class TestSettings(unittest.TestCase):

    layer = IMIO_FPAUDIT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_validate_settings(self):
        """Check invariant"""
        invariants = validator.InvariantsValidator(None, None, None, IFPAuditSettings, None)
        # test id uniqueness
        data = {
            "log_entries": [
                {"log_id": u"a", "audit_log": u"a.log", "log_format": u"%(asctime)s - %(message)s"},
                {"log_id": u"b", "audit_log": u"b.log", "log_format": u"%(asctime)s - %(message)s"},
            ]
        }
        self.assertFalse(invariants.validate(data))
        data = {
            "log_entries": [
                {"log_id": u"a", "audit_log": u"a.log", "log_format": u"%(asctime)s - %(message)s"},
                {"log_id": u"a", "audit_log": u"b.log", "log_format": u"%(asctime)s - %(message)s"},
            ]
        }
        errors = invariants.validate(data)
        self.assertTrue(isinstance(errors[0], Invalid))

    def test_settings_changed(self):
        """Check event"""
        api.portal.set_registry_record("imio.fpaudit.settings.log_entries", [])
        storage = getUtility(ILogsStorage)
        self.assertDictEqual(storage.storage, {})
        self.assertIsNone(storage.get("a"))
        api.portal.set_registry_record(
            "imio.fpaudit.settings.log_entries",
            [{"log_id": u"a", "audit_log": u"a.log", "log_format": u"%(asctime)s - %(message)s"}],
        )
        log_i = storage.get("a")
        self.assertIsNotNone(log_i)
        self.assertTrue(isinstance(log_i, FPAuditLogInfo))
