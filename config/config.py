import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TOKEN_CLICKUP")
url_space = os.getenv("URL_SPACE")
url_base = os.getenv("URL_BASE")

headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}
