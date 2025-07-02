import json
import logging

import allure
import pytest
import requests
from faker import Faker

from config.config import headers, url_base, url_space, url_space_non_existent_team
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from src.api.conftest import create_space, test_log_name
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

@allure.story("Spaces")
@allure.parent_suite("Space")
class TestSpace:
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
    @allure.title("Test Create Space")
    @allure.tag("acceptance", "smoke")
    @allure.label("owner", "Esther Huarayo")
    def test_create_space(self, test_log_name):
        """
        Test create space
        :param test_log_name: log the test name
        """
        # body
        space_body = {
            "name": f"Space {self.faker.company()} ",
        }
        response = self.rest_client.send_request(
            "POST", url=f"{url_space}", headers=headers, body=space_body
        )
        LOGGER.debug("Response: %s", json.dumps(response["body"], indent=4))
        LOGGER.debug("Status Code: %s", str(response["status_code"]))
        self.space_list.append(response["body"]["id"])
        # assertion
        self.validate.validate_value(response["status_code"], 200, "status_code")

    @pytest.mark.acceptance
    @allure.title("Test Get Space")
    @allure.tag("acceptance")
    @allure.label("owner", "Esther Huarayo")
    def test_get_space(self, create_space, test_log_name):
        """
        Test get space
        :param create_space: (str) Space id
        :param test_log_name: (str) log the test name
        """
        space_id = create_space
        response = self.rest_client.send_request(
            "GET", url=f"{url_base}/{space_id}", headers=headers)
        LOGGER.debug("Response: %s", response["body"])
        LOGGER.debug("Status Code: %s", str(response["status_code"]))
        # assertion
        self.validate.validate_value(response["status_code"], 200, "status_code")

    @pytest.mark.acceptance
    @allure.title("Test Update Space")
    @allure.tag("acceptance")
    @allure.label("owner", "Esther Huarayo")
    def test_update_space(self, create_space, test_log_name):
        """
        Test update space
        :param create_space: (str) Space id
        :param test_log_name: (str) log the test name
        """
        space_id = create_space
        #body for update space
        update_space_body = {
            "name": "Test ClickUp Space Updated ",
        }
        response = requests.put(
            url=f"{url_base}/{space_id}", headers=headers, json=update_space_body
        )
        LOGGER.debug("Response: %s", json.dumps(response.json(), indent=4))
        LOGGER.debug("Status Code: %s", str(response.status_code))
        # assertion
        self.validate.validate_value(response.status_code, 200, "status_code")

    @pytest.mark.acceptance
    @allure.title("Test Delete Space")
    @allure.tag("acceptance")
    @allure.label("owner", "Esther Huarayo")
    def test_delete_space(self, create_space, test_log_name):
        """
        Test delete space
        :param create_space: (str) Space id
        :param test_log_name: (str) log the test name
        """
        space_id = create_space
        response = self.rest_client.send_request("DELETE", url=f"{url_base}/{space_id}", headers=headers)
        # assertion
        self.validate.validate_response(response, "delete_space")

    @pytest.mark.functional
    @allure.title("Test Validate error message when trying to create space without name")
    @allure.tag("functional")
    @allure.label("owner", "Esther Huarayo")
    def test_create_space_without_body(self, test_log_name):
        """
        Test create space without body
        :param test_log_name:
        :return:
        """
        response = self.rest_client.send_request(
            "POST", url=url_space, headers=headers
        )
        LOGGER.debug("Response: %s", json.dumps(response['body'], indent=4))
        LOGGER.debug("Status Code: %s", str(response['status_code']))
        # assertion
        self.validate.validate_response(response, "create_space_without_body")

    @pytest.mark.functional
    @allure.title("Test Validate different inputs in Space name")
    @allure.tag("functional")
    @allure.label("owner", "Esther Huarayo")
    @pytest.mark.parametrize("name_space_test", ["#@-*!", "Space/Name&", "A" * 255])
    def test_create_space_using_different_name_space(self, test_log_name, name_space_test):
        """
        Test create space
        :param test_log_name: log the test name
        """
        space_body = {
            "name": f"{name_space_test}",
        }
        response = self.rest_client.send_request(
            "POST", url=f"{url_space}", headers=headers, body=space_body
        )
        LOGGER.debug("Response: %s", json.dumps(response["body"], indent=4))
        LOGGER.debug("Status Code: %s", str(response["status_code"]))
        self.space_list.append(response["body"]["id"])
        # assertion
        self.validate.validate_value(response["status_code"], 200, "status_code")

    @pytest.mark.functional
    @allure.title("Test Create Space in non existent team")
    @allure.tag("functional")
    @allure.label("owner", "Esther Huarayo")
    def test_create_space_in_non_existent_team(self, test_log_name):
        """
        Test create space in non existent team
        :param test_log_name: log the test name
        """
        space_body = {
            "name": f"Space {self.faker.company()} ",
        }
        response = self.rest_client.send_request(
            "POST", url=f"{url_space_non_existent_team}", headers=headers, body=space_body
        )
        LOGGER.debug("Response: %s", json.dumps(response["body"], indent=4))
        LOGGER.debug("Status Code: %s", str(response["status_code"]))
        # assertion
        self.validate.validate_response(response, "create_space_non_existent_team")

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
