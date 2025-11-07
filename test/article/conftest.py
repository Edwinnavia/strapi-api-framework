import pytest
from main.hooks.article_hooks import ArticleHooks
from data.articles import generate_article_payload


@pytest.fixture
def article_factory(strapi_api):
    created_ids = []

    def _create_article(payload=None):
        payload = payload or generate_article_payload()
        response = ArticleHooks.before_create(strapi_api, payload)

        try:
            result = response.json()
        except ValueError:
            pytest.fail(f"Failed to decode JSON response: {response.text}")

        if "data" not in result or "documentId" not in result["data"]:
            pytest.fail(f"Unexpected response structure while creating article: {result}")

        document_id = result["data"]["documentId"]
        created_ids.append(document_id)
        return result["data"]

    yield _create_article

    for document_id in created_ids:
        ArticleHooks.after_delete(strapi_api, document_id)


@pytest.fixture
def setup_teardown_article(article_factory):
    article = article_factory()
    yield article


@pytest.fixture(scope="module")
def module_article(strapi_api):
    payload = generate_article_payload()
    response = ArticleHooks.before_create(strapi_api, payload)

    try:
        result = response.json()
    except ValueError:
        pytest.fail("Invalid JSON response while creating module article")

    document_id = result["data"]["documentId"]

    yield result["data"]

    ArticleHooks.after_delete(strapi_api, document_id)
