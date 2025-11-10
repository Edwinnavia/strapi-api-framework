import pytest

from data.categories import generate_category_payload
from main.hooks.category_hooks import CategoryHooks
from main.strapi_api import StrapiApi
from main.hooks.article_hooks import ArticleHooks
from main.hooks.author_hooks import AuthorHooks
from data.articles import generate_article_payload
from data.authors import generate_author_payload


@pytest.fixture(scope="session")
def strapi_api():
    return StrapiApi()

@pytest.fixture(scope="session")
def module_article_session(strapi_api):
    payload = generate_article_payload(author=1)
    response = ArticleHooks.before_create(strapi_api, payload)

    try:
        data = response.json()["data"]
    except ValueError:
        pytest.fail("Invalid JSON response creating module article")

    yield data
    ArticleHooks.after_delete(strapi_api, data["documentId"])


@pytest.fixture(scope="session")
def module_author_session(strapi_api, module_article_session):
    payload = generate_author_payload(
        articles=[module_article_session["documentId"]],
        avatar=7
    )

    response = AuthorHooks.before_create(strapi_api, payload)

    try:
        data = response.json()["data"]
    except ValueError:
        pytest.fail("Invalid JSON response creating module author")

    yield data
    AuthorHooks.after_delete(strapi_api, data["documentId"])


@pytest.fixture(scope="session")
def module_category_session(strapi_api, module_article_session):
    payload = generate_category_payload(
        articles=[{"documentId": module_article_session["documentId"]}]
    )

    response = CategoryHooks.before_create(strapi_api, payload)

    try:
        result = response.json()
    except ValueError:
        pytest.fail("Invalid JSON response creating module category")

    document_id = result["data"]["documentId"]

    yield result["data"]

    CategoryHooks.after_delete(strapi_api, document_id)
