import logging
from hnt_jira.attachment.jira_api import JiraAPI
from hnt_jira.constants import DEST_PATH

logger = logging.getLogger(__name__)

class JiraService():
    def __init__(self) -> None:
        pass

    def download_attachment(self, content_id, filename, dest_path = DEST_PATH):
        return JiraAPI().download_attachment(content_id, filename, dest_path)
        