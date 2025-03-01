import logging
import os
from dotenv import load_dotenv
import requests
from hnt_jira.constants import JIRA_AUTH

logger = logging.getLogger(__name__)

class JiraAPI:
    def __init__(self) -> None:
        load_dotenv()
        pass
    def download_attachment(self, content_id, filename, dest_path):
        logger.info(f"Enter download_attachment method")        
        res = requests.get(
            url=f"https://hnt.atlassian.net/rest/api/3/attachment/content/{content_id}",
            timeout=10,
            auth=JIRA_AUTH,
            allow_redirects=True)
        res.raise_for_status()
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        dest_path_filename = os.path.join(dest_path, filename)
        open(dest_path_filename, 'wb').write(res.content)
        logger.info(f"Leave download_attachment method, dest_path_filename: {dest_path_filename}")
        return dest_path_filename