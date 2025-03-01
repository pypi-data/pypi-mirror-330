# -*- coding: utf-8 -*-
from collective.fingerpointing.utils import get_request_information
from file_read_backwards import FileReadBackwards
from imio.fpaudit.interfaces import ILogsStorage
from natsort import natsorted
from plone import api
from zope.component import getUtility

import logging
import os
import re


logger = logging.getLogger("imio.fpaudit")
AUDIT_MESSAGE = u'user={0} ip={1} action={2} {3}'


def fplog(log_id, action, extras):
    """collective.fingerpointing add log message.

    :param log_id: The log id as defined in the configuration
    :param action: The action string
    :param extras: The extras"""
    user, ip = get_request_information()
    storage = getUtility(ILogsStorage)
    log_i = storage.get(log_id)
    if log_i:
        log_i(AUDIT_MESSAGE.format(user, ip, action, extras))
    else:
        logger.info(AUDIT_MESSAGE.format(user, ip, action, extras))


def get_all_lines_of(logfiles, actions=()):
    """Get all lines of a list of log files.

    :param logfiles: The list of log files
    :param actions: An action list to search_on"""
    for logfile in logfiles:
        for line in get_lines_of(logfile, actions=actions):
            yield line


def get_lines_info(line, extras):
    """Get the columns info of a log line.

    :param line: The log line
    :param extras: The extras tags list
    :return: A dictionary with the columns info"""
    dic = {}
    # 24-10-10 14:59:07 - user=admin ip=127.0.0.1 action=AUDIT col_a=xxxx col_b=yyy
    pattern = (
        r"(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - user=(?P<user>.+?) "
        r"ip=(?P<ip>[\d\.]+|None) action=(?P<action>.+?)"
    )

    for extra in extras:
        pattern += r" {}=(?P<{}>.+?)".format(extra, extra)

    pattern += r"$"
    match = re.match(pattern, line)
    if match:
        dic = match.groupdict()
    else:
        dic["_line_"] = line
    return dic


def get_lines_of(logfile, actions=()):
    """Generator for reversed log lines of a log file.

    :param logfile: The path to the log file
    :param actions: An action list to search_on"""
    acts = [" action={}".format(act) for act in actions]
    with FileReadBackwards(logfile, encoding="utf-8") as file:
        for line in file:
            s_line = line.strip("\n")
            if not actions or any(act in s_line for act in acts):
                yield s_line


def get_log_option(log_id, option):
    """Get option value from settings

    :param log_id: The log id as defined in the configuration
    :param option: The option name"""
    log_entries = api.portal.get_registry_record("imio.fpaudit.settings.log_entries", default=[])
    for entry in log_entries:
        if entry["log_id"] == log_id:
            return entry.get(option)


def get_logrotate_filenames(directory, base_filename, suffix_regex=r"\.\d+$", full=True):
    """Get all logrotate files matching the base filename in the directory.

    :param directory: The directory where the logrotate files are stored
    :param base_filename: The base filename of the logrotate files
    :param suffix_regex: The regex pattern to match the suffix of the logrotate files
    :param full: If True, return the full path of the logrotate files
    """
    pattern = re.compile("^{}(?:{})*$".format(re.escape(base_filename), suffix_regex))
    res = natsorted([f for f in os.listdir(directory) if pattern.match(f)])
    if full:
        res = [os.path.join(directory, f) for f in res]
    return res
