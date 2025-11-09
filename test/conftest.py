import pytest
from main.strapi_api import StrapiApi
from main.hooks.article_hooks import ArticleHooks
from main.hooks.author_hooks import AuthorHooks
from data.articles import generate_article_payload
from data.authors import generate_author_payload


@pytest.fixture(scope="session")
def strapi_api():
    return StrapiApi()


@pytest.fixture(scope="session")
def module_article(strapi_api):
    payload = generate_article_payload(author=1)
    response = ArticleHooks.before_create(strapi_api, payload)
    data = response.json()["data"]
    yield data
    ArticleHooks.after_delete(strapi_api, data["documentId"])


@pytest.fixture(scope="session")
def module_author(strapi_api, module_article):
    payload = generate_author_payload(
        articles=[module_article["documentId"]],
        avatar=7
    )
    response = AuthorHooks.before_create(strapi_api, payload)
    data = response.json()["data"]
    yield data
    AuthorHooks.after_delete(strapi_api, data["documentId"])
