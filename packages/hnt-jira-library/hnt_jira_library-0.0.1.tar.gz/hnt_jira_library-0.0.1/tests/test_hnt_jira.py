import os
from hnt_jira import JiraService
from hnt_jira.constants import DEST_PATH

def test_download_FIN_51663():
    filename = 'Taxa VISA_Ano 2025_Ammericanas Praia da Costa.pdf'
    dest_path_filename = JiraService().download_attachment(
        content_id='551565',
        filename=filename)
    expected = os.path.join(DEST_PATH, filename) 
    assert dest_path_filename == expected

def test_download_FIN_51664():
    filename = 'Taxa_fisalização anual_ano 2025_Americanas Praia da Costa.pdf'
    dest_path_filename = JiraService().download_attachment(
        content_id='551566',
        filename=filename)
    expected = os.path.join(DEST_PATH, filename) 
    assert dest_path_filename == expected
