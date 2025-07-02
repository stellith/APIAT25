import json
import logging

import allure
import pytest
import requests
from faker import Faker

from config.config import url_base, headers, url_folder
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from src.api.conftest import create_space, test_log_name
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.story("Folder")
@allure.parent_suite("Folder")
class TestFolder:
    @classmethod
    def setup_class(cls):
        """
        Setup before all tests
        :return:
        """
        # Arrange
        cls.folder_list = []
        cls.space_list = []
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.faker = Faker()

    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("Test Create Folder")
    @allure.tag("acceptance", "smoke")
    @allure.label("owner", "Esther Huarayo")
    def test_create_folder(self, test_log_name, create_space):
        """
        Test for create a Folder
        :param test_log_name:  log the test name
        """
        space_id = create_space
        # body
        folder_body = {
            "name": f"Folder {self.faker.company()}"
        }
        # call endpoint using requests
        response = self.rest_client.send_request(
            "POST", url=f"{url_base}{space_id}/folder", headers=headers, body=folder_body
        )
        LOGGER.debug("Response: %s", json.dumps(response["body"], indent=4))
        LOGGER.debug("Status Code: %s", str(response["status_code"]))
        self.space_list.append(space_id)
        # assertion
        self.validate.validate_value(response["status_code"], 200, "status_code")

    @pytest.mark.acceptance
    @allure.title("Test Get Folder")
    @allure.tag("acceptance")
    @allure.label("owner", "Esther Huarayo")
    def test_get_folder(self, create_folder, test_log_name):
        """
        Test get folder
        :param create_folder: (str) Folder id
        :param test_log_name: (str) log the test name
        """
        folder_id, space_id = create_folder
        response = self.rest_client.send_request(
            "GET", url=f"{url_folder}/{folder_id}", headers=headers)
        LOGGER.debug("Response: %s", response["body"])
        LOGGER.debug("Status Code: %s", str(response["status_code"]))
        self.space_list.append(space_id)
        # assertion
        self.validate.validate_value(response["status_code"], 200, "status_code")

    @pytest.mark.acceptance
    @allure.title("Test Update Folder")
    @allure.tag("acceptance")
    @allure.label("owner", "Esther Huarayo")
    def test_update_folder(self, create_folder, test_log_name):
        """
        Test update folder
        :param create_folder: (str) Folder id
        :param test_log_name: (str) log the test name
        """
        folder_id, space_id = create_folder
        #body for update space
        update_folder_body = {
            "name": "Folder Updated",
        }
        response = requests.put(
            url=f"{url_folder}/{folder_id}", headers=headers, json=update_folder_body
        )
        LOGGER.debug("Response: %s", json.dumps(response.json(), indent=4))
        LOGGER.debug("Status Code: %s", str(response.status_code))
        self.space_list.append(space_id)
        # assertion
        self.validate.validate_value(response.status_code, 200, "status_code")

    @pytest.mark.acceptance
    @allure.title("Test Delete Folder")
    @allure.tag("acceptance")
    @allure.label("owner", "Esther Huarayo")
    def test_delete_folder(self, create_folder, test_log_name):
        """
        Test delete folder
        :param create_folder: (str) Space id
        :param test_log_name: (str) log the test name
        """
        folder_id, space_id = create_folder
        response = self.rest_client.send_request("DELETE", url=f"{url_folder}/{folder_id}", headers=headers)
        self.space_list.append(space_id)
        # assertion
        self.validate.validate_response(response, "delete_folder")

    @classmethod
    def teardown_class(cls):
        """
        Clean up after all tests
        :return:
        """
        # Cleanup Folder
        LOGGER.info("Test Folder teardown Class")
        for space_id in cls.space_list:
            response = requests.delete(url=f"{url_base}/{space_id}", headers=headers)
            LOGGER.debug("Status Code: %s", str(response.status_code))
            if response.status_code == 200:
                LOGGER.debug("Space Folder deleted")
