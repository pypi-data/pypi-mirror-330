import os

#PATH
DEST_PATH = os.path.join(os.getcwd(), "output", "pdf")
JIRA_AUTH = (os.getenv("USER"), os.getenv("ACCESS_TOKEN"))