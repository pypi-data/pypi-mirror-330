# -*- coding: utf-8 -*-
from imio.fpaudit import LOG_DIR
from imio.fpaudit.storage import store_config
from imio.fpaudit.testing import clear_temp_dir
from imio.fpaudit.testing import IMIO_FPAUDIT_INTEGRATION_TESTING
from imio.fpaudit.testing import write_temp_files
from imio.fpaudit.utils import fplog
from imio.fpaudit.utils import get_all_lines_of
from imio.fpaudit.utils import get_lines_info
from imio.fpaudit.utils import get_lines_of
from imio.fpaudit.utils import get_logrotate_filenames
from plone import api

import os
import shutil
import tempfile
import unittest


class TestUtils(unittest.TestCase):

    layer = IMIO_FPAUDIT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_fplog(self):
        api.portal.set_registry_record(
            "imio.fpaudit.settings.log_entries",
            [{"log_id": u"test", "audit_log": u"test_utils.log", "log_format": u"%(asctime)s - %(message)s"}],
        )
        log_file_path = os.path.join(LOG_DIR, "test_utils.log")
        for fil in get_logrotate_filenames(LOG_DIR, "test_utils.log", r".+$"):
            os.remove(fil)
        fplog("test", "AUDIT", "extra 1")
        logs = get_logrotate_filenames(LOG_DIR, "test_utils.log", r"\.\d+$")
        self.assertListEqual(logs, [log_file_path])
        lines = [ln for ln in get_lines_of(log_file_path)]
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].endswith(" - user=test_user_1_ ip=None action=AUDIT extra 1"))
        fplog("test", "AUDIT", "extra 2")
        lines = [ln for ln in get_lines_of(log_file_path)]
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].endswith(" - user=test_user_1_ ip=None action=AUDIT extra 2"))
        self.assertTrue(lines[1].endswith(" - user=test_user_1_ ip=None action=AUDIT extra 1"))
        # check with logrotated files
        log_file_path1 = log_file_path + ".1"
        os.rename(log_file_path, log_file_path1)
        # changed id to stop writing in rotated here
        store_config([{"log_id": u"test1", "audit_log": u"test_utils.log", "log_format": u"%(asctime)s - %(message)s"}])
        fplog("test1", "AUDIT", "extra 3")
        fplog("test1", "AUDIT", "extra 4")
        logs = get_logrotate_filenames(LOG_DIR, "test_utils.log", r"\.\d+$")
        lines = [ln for ln in get_all_lines_of(logs)]
        self.assertTrue(lines[0].endswith(" - user=test_user_1_ ip=None action=AUDIT extra 4"))
        self.assertTrue(lines[1].endswith(" - user=test_user_1_ ip=None action=AUDIT extra 3"))
        self.assertTrue(lines[2].endswith(" - user=test_user_1_ ip=None action=AUDIT extra 2"))
        self.assertTrue(lines[3].endswith(" - user=test_user_1_ ip=None action=AUDIT extra 1"))
        for fil in get_logrotate_filenames(LOG_DIR, "test_utils.log", r".+$"):
            os.remove(fil)

    def test_get_lines_info(self):
        line = "2024-10-10 14:59:07 - user=admin ip=127.0.0.1 action=AUDIT col_a=xx  xx col_b=yyy éé"
        dic = get_lines_info(line, ["col_a", "col_b"])
        self.assertDictEqual(
            dic,
            {
                "date": "2024-10-10 14:59:07",
                "user": "admin",
                "ip": "127.0.0.1",
                "action": "AUDIT",
                "col_a": "xx  xx",
                "col_b": "yyy éé",
            },
        )

    def test_get_lines_of(self):
        api.portal.set_registry_record(
            "imio.fpaudit.settings.log_entries",
            [{"log_id": u"test", "audit_log": u"test_utils.log", "log_format": u"%(asctime)s - %(message)s"}],
        )
        log_file_path = os.path.join(LOG_DIR, "test_utils.log")
        for fil in get_logrotate_filenames(LOG_DIR, "test_utils.log", r".+$"):
            os.remove(fil)
        fplog("test", "AUDIT", "extra")
        fplog("test", "CONTACTS", "extra")
        fplog("test", "CONTACTS", "extra")
        fplog("test", "AUDIT", "extra")
        fplog("test", "GROUPS", "extra")
        lines = [ln for ln in get_lines_of(log_file_path)]
        self.assertEqual(len(lines), 5)
        lines = [ln for ln in get_lines_of(log_file_path, actions=("GROUPS",))]
        self.assertEqual(len(lines), 1)
        self.assertTrue(all("GROUPS" in ln for ln in lines))
        lines = [ln for ln in get_lines_of(log_file_path, actions=("AUDIT", "CONTACTS"))]
        self.assertEqual(len(lines), 4)
        self.assertEqual(len([ln for ln in lines if "AUDIT" in ln]), 2)
        self.assertEqual(len([ln for ln in lines if "CONTACTS" in ln]), 2)
        for fil in get_logrotate_filenames(LOG_DIR, "test_utils.log", r".+$"):
            os.remove(fil)

    def test_get_logrotate_filenames(self):
        temp_dir = tempfile.mkdtemp()
        try:
            # check filter
            write_temp_files(temp_dir, ["test.log", "other.log", "test.log.1", "test.log.2", "test.log.lock"])
            expected_files = ["test.log", "test.log.1", "test.log.2"]
            result_files = get_logrotate_filenames(temp_dir, "test.log", r"\.\d+$", full=False)
            self.assertListEqual(result_files, expected_files)
            clear_temp_dir(temp_dir)
            # check order
            write_temp_files(temp_dir, ["test.log", "test.log.1", "test.log.2", "test.log.10"])
            expected_files = ["test.log", "test.log.1", "test.log.2", "test.log.10"]
            result_files = get_logrotate_filenames(temp_dir, "test.log", r"\.\d+$", full=False)
            self.assertListEqual(result_files, expected_files)
            clear_temp_dir(temp_dir)
            # check full path
            write_temp_files(temp_dir, ["test.log", "test.log.1", "test.log.2", "test.log.10"])
            expected_files = ["test.log", "test.log.1", "test.log.2", "test.log.10"]
            expected_files = [os.path.join(temp_dir, f) for f in expected_files]
            result_files = get_logrotate_filenames(temp_dir, "test.log", r"\.\d+$")
            self.assertListEqual(result_files, expected_files)
            clear_temp_dir(temp_dir)
            # checl another filter
            write_temp_files(
                temp_dir, ["test.log", "other.log", "test.log-20240825", "test.log-20240901", "test.log-20240908"]
            )
            expected_files = ["test.log", "test.log-20240825", "test.log-20240901", "test.log-20240908"]
            result_files = get_logrotate_filenames(temp_dir, "test.log", r"-\d{8}$", full=False)
            self.assertListEqual(result_files, expected_files)
        finally:
            shutil.rmtree(temp_dir)
