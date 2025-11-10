import pytest
from main.hooks.category_hooks import CategoryHooks
from data.categories import generate_category_payload


@pytest.fixture
def category_factory(strapi_api):
    created_ids = []

    def _create_category(payload=None):
        payload = payload or generate_category_payload()
        response = CategoryHooks.before_create(strapi_api, payload)

        try:
            result = response.json()
        except ValueError:
            pytest.fail(f"Failed to decode JSON response while creating category: {response.text}")

        if "data" not in result or "documentId" not in result["data"]:
            pytest.fail(f"Unexpected response structure while creating category: {result}")

        document_id = result["data"]["documentId"]
        created_ids.append(document_id)
        return result["data"]

    yield _create_category

    for document_id in created_ids:
        CategoryHooks.after_delete(strapi_api, document_id)


@pytest.fixture
def setup_teardown_category(category_factory):
    category = category_factory()
    yield category


@pytest.fixture(scope="module")
def module_category(strapi_api, module_article_session):
    payload = generate_category_payload(
        articles=[
            {"documentId": module_article_session["documentId"]}
        ]
    )

    response = CategoryHooks.before_create(strapi_api, payload)

    try:
        result = response.json()
    except ValueError:
        pytest.fail("Invalid JSON response while creating module category")

    document_id = result["data"]["documentId"]

    yield result["data"]

    CategoryHooks.after_delete(strapi_api, document_id)


@pytest.fixture
def teardown_category(strapi_api):
    created_ids = []
    yield created_ids

    for document_id in created_ids:
        CategoryHooks.after_delete(strapi_api, document_id)
