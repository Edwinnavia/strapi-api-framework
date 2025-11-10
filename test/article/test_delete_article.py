import pytest
from main.endpoints.article_endpoint import ArticleEndpoint
from main.validation_manager import ValidationManager
from data.articles import generate_article_payload

validate = ValidationManager()
pytestmark = pytest.mark.delete_article


# ============================================================
# TC-DA-01 - Delete article with valid documentId
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_delete_article_valid(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    url = ArticleEndpoint.delete(article["documentId"])
    response = strapi_api.delete(url)

    validate.status.no_content(response)


# ============================================================
# TC-DA-02 - Delete without auth token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_delete_article_missing_auth(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    url = ArticleEndpoint.delete(article["documentId"])
    response = strapi_api.delete(url, with_auth=False)

    validate.status.forbidden(response)


# ============================================================
# TC-DA-03 - Delete with invalid token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_delete_article_invalid_token(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    url = ArticleEndpoint.delete(article["documentId"])
    headers = {"Authorization": "Bearer INVALID123"}

    response = strapi_api.delete(url, headers=headers)
    validate.status.unauthorized(response)


# ============================================================
# TC-DA-04 - Delete with empty Authorization header
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_delete_article_empty_auth_header(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    url = ArticleEndpoint.delete(article["documentId"])
    headers = {"Authorization": ""}

    response = strapi_api.delete(url, headers=headers)
    validate.status.forbidden(response)


# ============================================================
# TC-DA-05 - Delete nonexistent documentId
# BUG: Strapi devuelve 204 en lugar de 404 cuando el documentId no existe
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi devuelve 204 en vez de 404 al eliminar un documentId inexistente", strict=False)
def test_delete_article_nonexistent(strapi_api):
    url = ArticleEndpoint.delete("aasaqw7878")

    response = strapi_api.delete(url)

    validate.status.not_found(response)


# ============================================================
# TC-DA-06 - Delete with empty documentId ""
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_delete_article_empty_documentId(strapi_api):
    url = ArticleEndpoint.delete("")

    response = strapi_api.delete(url)
    validate.status.method_not_allowed(response)


# ============================================================
# TC-DA-07 - Delete already deleted article
# BUG: Strapi permite eliminar dos veces el mismo documentId
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi permite eliminar dos veces el mismo article en vez de retornar 404",
                   strict=False)
def test_delete_article_twice(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    url = ArticleEndpoint.delete(article["documentId"])
    first = strapi_api.delete(url)
    validate.status.no_content(first)

    second = strapi_api.delete(url)
    validate.status.not_found(second)


# ============================================================
# TC-DA-08 - Delete then GET should return 404
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_delete_article_then_get(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    url_delete = ArticleEndpoint.delete(article["documentId"])
    response_delete = strapi_api.delete(url_delete)
    validate.status.no_content(response_delete)

    url_get = ArticleEndpoint.get_by_id(article["documentId"])
    response_get = strapi_api.get(url_get)

    validate.status.not_found(response_get)


# ============================================================
# TC-DA-09 - Concurrency: multiple DELETE at same time
# BUG: Strapi permite borrar dos veces en concurrencia sin retornar 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi devuelve 204 en ambos DELETE concurrentes en vez de 404 en el segundo",
                   strict=False)
def test_delete_article_concurrent(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    url = ArticleEndpoint.delete(article["documentId"])

    r1 = strapi_api.delete(url)
    r2 = strapi_api.delete(url)

    validate.status.no_content(r1)
    validate.status.not_found(r2)
