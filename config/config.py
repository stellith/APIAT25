import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TOKEN_CLICKUP")
url_space = os.getenv("URL_SPACE")
url_space_non_existent_team = os.getenv("URL_SPACE_NON_EXISTENT_TEAM")
url_base = os.getenv("URL_BASE")
url_teams = os.getenv("URL_TEAMS")
web_hook = os.getenv("WEB_HOOK")
url_folder = os.getenv("URL_FOLDER")
url_list = os.getenv("URL_LIST")

headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}
