import json
import logging
import requests
from config.config import headers, url_base, url_space
from src.api.conftest import create_space, test_log_name
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestSpace:
    def test_create_space(self, test_log_name):
        space_body = {
            "name": "Test ClickUp Space ",
        }
        response = requests.post(
            url=f"{url_space}", headers=headers, json=space_body
        )
        LOGGER.debug("Response: %s", json.dumps(response.json(), indent=4))
        LOGGER.debug("Status Code: %s", str(response.status_code))
        assert response.status_code == 200

    def test_get_space(self, create_space, test_log_name):
        space_id = create_space
        response = requests.get(url=f"{url_base}/{space_id}", headers=headers)
        LOGGER.debug("Response: %s", response.json())
        LOGGER.debug("Status Code: %s", str(response.status_code))
        assert response.status_code == 200

    def test_update_space(self, create_space, test_log_name):
        space_id = create_space
        update_space_body = {
            "name": "Test ClickUp Space Updated ",
        }
        response = requests.put(
            url=f"{url_base}/{space_id}", headers=headers, json=update_space_body
        )
        LOGGER.debug("Response: %s", json.dumps(response.json(), indent=4))
        LOGGER.debug("Status Code: %s", str(response.status_code))
        assert response.status_code == 200

    def test_delete_space(self, create_space, test_log_name):
        space_id = create_space
        response = requests.delete(url=f"{url_base}/{space_id}", headers=headers)
        LOGGER.debug("Response: %s", response.json())
        LOGGER.debug("Status Code: %s", str(response.status_code))
        assert response.status_code == 200
