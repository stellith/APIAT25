import json
import logging

import allure
import pytest
import requests
from faker import Faker

from config.config import headers, url_base, url_space, url_space_non_existent_team, url_folder
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from src.api.conftest import create_space, test_log_name
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

@allure.story("E2E")
@allure.parent_suite("E2E")
class TestE2E:
    @classmethod
    def setup_class(cls):
        """
        Setup before all tests
        :return:
        """

        # Arrange
        cls.space_list = []
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.faker = Faker()

    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("E2E Test: Create Space, Folder, and List")
    @allure.tag("acceptance", "smoke")
    @allure.label("owner", "Esther Huarayo")
    def test_create_list_e2e(self, test_log_name, create_folder):
        """
        End-to-end test: Create a space, a folder in that space, and a list in the folder.
        :param test_log_name: log the test name
        """
        folder_id, space_id = create_folder

        # --- Step 1: Create List ---
        list_name = f"E2E List {self.faker.company()}"
        list_body = {
            "name": list_name
        }

        response = self.rest_client.send_request(
            "POST", url=f"{url_folder}{folder_id}/list", headers=headers, body=list_body
        )

        LOGGER.debug("Response: %s", json.dumps(response["body"], indent=4))
        LOGGER.debug("Status Code: %s", str(response["status_code"]))

        # Save for cleanup
        self.space_list.append(space_id)

        # assertions
        assert response["body"]["name"] == list_name, "List name mismatch"
        self.validate.validate_value(response["status_code"], 200, "status_code")


    @classmethod
    def teardown_class(cls):
        """
        Clean up after all tests
        :return:
        """
        # Cleanup spaces
        LOGGER.info("Test Space teardown Class")
        for space_id in cls.space_list:
            response = requests.delete(url=f"{url_base}/{space_id}", headers=headers)
            LOGGER.debug("Status Code: %s", str(response.status_code))
            if response.status_code == 200:
                LOGGER.debug("Space deleted")
