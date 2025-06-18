import pytest
import logging
import requests

from config.config import url_space, headers
from utils.logger import get_logger
from faker import Faker

LOGGER = get_logger(__name__, logging.DEBUG)

# Create an instance of Faker to generate random data
fake = Faker()

# Function to generate a random name using Faker
def create_random_name():
    return fake.company()

# Function to generate a random name using Faker
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
    return space_id

@pytest.fixture
def test_log_name(request):
    LOGGER.info(f"Start test '{request.node.name}'")

    def fin():
        LOGGER.info(f"End test '{request.node.name}'")

    request.addfinalizer(fin)
