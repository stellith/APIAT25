import pytest
import logging
import requests

from config.config import url_space, headers, url_base, url_folder, url_list
from utils.logger import get_logger
from faker import Faker

LOGGER = get_logger(__name__, logging.DEBUG)

# Create an instance of Faker to generate random data
fake = Faker()

# Function to generate a random name using Faker
def create_random_name():
    return fake.company()

# Arrange
@pytest.fixture
def create_space():
    LOGGER.info("Creating a new ClickUp Space...")

    space_name = create_random_name()
    # space body
    space_body = {
        "name": space_name
    }

    # call endpoint using requests
    response = requests.post(
        url=f"{url_space}", headers=headers, json=space_body
    )
    LOGGER.debug(response.json())

    # get id space
    space_id = response.json()["id"]
    LOGGER.info(f"Space id: {space_id}")
    yield space_id

    delete_space(space_id)

# Arrange
@pytest.fixture
def test_log_name(request):
    LOGGER.info(f"Start test '{request.node.name}'")

    def fin():
        LOGGER.info(f"End test '{request.node.name}'")

    request.addfinalizer(fin)

def delete_space(space_id):
    LOGGER.info(f"Delete space fixture: {space_id}")
    response = requests.delete(url=f"{url_base}/{space_id}", headers=headers)
    LOGGER.debug("Response: %s", response.json())
    LOGGER.debug("Status Code: %s", str(response.status_code))
    if response.status_code == 200:
        LOGGER.debug("Space deleted")

@pytest.fixture()
def create_folder(create_space):
    LOGGER.debug("Create folder fixture")

    space_id = create_space
    folder_name = create_random_name()
    folder_body = {
        "name": folder_name
    }
    response = requests.post(
        url=f"{url_base}{space_id}/folder", headers=headers, json=folder_body
    )
    LOGGER.debug(response.json())

    # get id folder
    folder_id = response.json()["id"]
    LOGGER.info(f"Folder id: {folder_id}")
    yield folder_id, space_id

    delete_folder(folder_id)

def delete_folder(folder_id):
    LOGGER.info(f"Delete folder fixture: {folder_id}")
    response = requests.delete(url=f"{url_folder}/{folder_id}", headers=headers)
    LOGGER.debug("Response: %s", response.json())
    LOGGER.debug("Status Code: %s", str(response.status_code))
    if response.status_code == 200:
        LOGGER.debug("Folder deleted")

@pytest.fixture()
def create_list(create_folder):
    LOGGER.debug("Create list fixture")
    folder_id, space_id = create_folder
    list_name = create_random_name()
    list_body = {
        "name": list_name
    }
    response = requests.post(
        url=f"{url_folder}{folder_id}/list", headers=headers, json=list_body
    )
    LOGGER.debug(response.json())

    # get id list
    list_id = response.json()["id"]
    LOGGER.info(f"List id: {list_id}")
    yield {
        "folder_id": folder_id,
        "space_id": space_id,
        "list_id": list_id
    }

    delete_folder(folder_id)

def delete_list(list_id):
    LOGGER.info(f"Delete list fixture: {list_id}")
    response = requests.delete(url=f"{url_list}/{list_id}", headers=headers)
    LOGGER.debug("Response: %s", response.json())
    LOGGER.debug("Status Code: %s", str(response.status_code))
    if response.status_code == 200:
        LOGGER.debug("List deleted")
