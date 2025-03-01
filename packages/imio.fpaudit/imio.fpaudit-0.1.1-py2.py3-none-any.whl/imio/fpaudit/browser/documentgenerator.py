from collective.documentgenerator.helper import DocumentGenerationHelperView
from imio.fpaudit import LOG_DIR
from imio.fpaudit.utils import get_all_lines_of
from imio.fpaudit.utils import get_lines_info
from imio.fpaudit.utils import get_log_option
from imio.fpaudit.utils import get_logrotate_filenames


class FPAuditHelperView(DocumentGenerationHelperView):
    """
    Helper methods used for document generation
    """

    def get_log_lines(self):
        """Get all lines of a list of log files.

        :param log_id: The log id as defined in the configuration
        :param actions: An action list to search_on"""
        log_id = self.context_var("log_id")
        actions = [act.strip() for act in self.context_var("actions", []).split(",")]
        extras = [extra.strip() for extra in self.context_var("extras", []).split(",")]
        logs = get_logrotate_filenames(LOG_DIR, get_log_option(log_id, "audit_log"), suffix_regex=r"\.\d+$", full=True)
        for line in get_all_lines_of(logs, actions=actions):
            yield get_lines_info(line, extras)
