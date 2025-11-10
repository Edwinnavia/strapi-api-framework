import pytest
from main.hooks.author_hooks import AuthorHooks
from data.authors import generate_author_payload


@pytest.fixture
def author_factory(strapi_api):
    created_ids = []

    def _create_author(payload=None):
        payload = payload or generate_author_payload()
        response = AuthorHooks.before_create(strapi_api, payload)

        try:
            result = response.json()
        except ValueError:
            pytest.fail(f"Failed to decode JSON response while creating author: {response.text}")

        if "data" not in result or "documentId" not in result["data"]:
            pytest.fail(f"Unexpected response structure while creating author: {result}")

        document_id = result["data"]["documentId"]
        created_ids.append(document_id)
        return result["data"]

    yield _create_author

    for document_id in created_ids:
        AuthorHooks.after_delete(strapi_api, document_id)


@pytest.fixture
def setup_teardown_author(author_factory):
    author = author_factory()
    yield author


@pytest.fixture(scope="module")
def module_author(strapi_api, module_article_session):
    payload = generate_author_payload(
        articles=[module_article_session["documentId"]]
    )

    response = AuthorHooks.before_create(strapi_api, payload)

    try:
        result = response.json()
    except ValueError:
        pytest.fail("Invalid JSON response while creating module author")

    document_id = result["data"]["documentId"]

    yield result["data"]

    AuthorHooks.after_delete(strapi_api, document_id)

@pytest.fixture
def teardown_author(strapi_api):
    created_ids = []
    yield created_ids

    for document_id in created_ids:
        AuthorHooks.after_delete(strapi_api, document_id)
