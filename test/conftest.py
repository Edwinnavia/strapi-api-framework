import pytest
from main.strapi_api import StrapiApi


@pytest.fixture(scope="session")
def strapi_api():
    return StrapiApi()
