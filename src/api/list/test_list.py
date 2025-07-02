import json
import logging

import allure
import pytest
import requests
from faker import Faker

from config.config import url_base, headers, url_list, url_folder
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from src.api.conftest import create_space, test_log_name
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.story("List")
@allure.parent_suite("List")
class TestList:
    @classmethod
    def setup_class(cls):
        """
        Setup before all tests
        :return:
        """
        # Arrange
        cls.list_list = []
        cls.space_list = []
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.faker = Faker()

    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("Test Create List")
    @allure.tag("acceptance", "smoke")
    @allure.label("owner", "Esther Huarayo")
    def test_create_list(self, test_log_name, create_folder):
        """
        Test for create a List
        :param test_log_name:  log the test name
        """
        folder_id, space_id = create_folder
        # body
        list_body = {
            "name": f"List {self.faker.company()}"
        }
        # call endpoint using requests
        response = self.rest_client.send_request(
            "POST", url=f"{url_folder}{folder_id}/list", headers=headers, body=list_body
        )
        LOGGER.debug("Response: %s", json.dumps(response["body"], indent=4))
        LOGGER.debug("Status Code: %s", str(response["status_code"]))
        self.space_list.append(space_id)
        # assertion
        self.validate.validate_value(response["status_code"], 200, "status_code")

    @pytest.mark.acceptance
    @allure.title("Test Get List")
    @allure.tag("acceptance")
    @allure.label("owner", "Esther Huarayo")
    def test_get_list(self, create_list, test_log_name):
        """
        Test get list
        :param create_list: (str) List id
        :param test_log_name: (str) log the test name
        """
        list_id = create_list["list_id"]
        space_id = create_list["space_id"]
        response = self.rest_client.send_request(
            "GET", url=f"{url_list}/{list_id}", headers=headers)
        LOGGER.debug("Response: %s", response["body"])
        LOGGER.debug("Status Code: %s", str(response["status_code"]))
        self.space_list.append(space_id)
        # assertion
        self.validate.validate_value(response["status_code"], 200, "status_code")

    @pytest.mark.acceptance
    @allure.title("Test Update List")
    @allure.tag("acceptance")
    @allure.label("owner", "Esther Huarayo")
    def test_update_list(self, create_list, test_log_name):
        """
        Test update list
        :param create_list: (str) List id
        :param test_log_name: (str) log the test name
        """
        list_id = create_list["list_id"]
        space_id = create_list["space_id"]
        #body for update list
        update_list_body = {
            "name": "List Updated",
        }
        response = requests.put(
            url=f"{url_list}/{list_id}", headers=headers, json=update_list_body
        )
        LOGGER.debug("Response: %s", json.dumps(response.json(), indent=4))
        LOGGER.debug("Status Code: %s", str(response.status_code))
        self.space_list.append(space_id)
        # assertion
        self.validate.validate_value(response.status_code, 200, "status_code")

    @pytest.mark.acceptance
    @allure.title("Test Delete List")
    @allure.tag("acceptance")
    @allure.label("owner", "Esther Huarayo")
    def test_delete_list(self, create_list, test_log_name):
        """
        Test delete list
        :param create_list: (str) list id
        :param test_log_name: (str) log the test name
        """
        list_id = create_list["list_id"]
        space_id = create_list["space_id"]
        response = self.rest_client.send_request("DELETE", url=f"{url_list}/{list_id}", headers=headers)
        self.space_list.append(space_id)
        # assertion
        self.validate.validate_response(response, "delete_list")

    @classmethod
    def teardown_class(cls):
        """
        Clean up after all tests
        :return:
        """
        # Cleanup List
        LOGGER.info("Test List teardown Class")
        for space_id in cls.space_list:
            response = requests.delete(url=f"{url_base}/{space_id}", headers=headers)
            LOGGER.debug("Status Code: %s", str(response.status_code))
            if response.status_code == 200:
                LOGGER.debug("Space List deleted")
