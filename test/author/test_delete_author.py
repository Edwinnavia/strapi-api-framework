import pytest
from main.endpoints.author_endpoint import AuthorEndpoint
from main.validation_manager import ValidationManager
from data.authors import generate_author_payload

validate = ValidationManager()
pytestmark = pytest.mark.delete_author


# ============================================================
# TC-DAU-01 - Delete author with valid documentId
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_delete_author_valid(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    url = AuthorEndpoint.delete(author["documentId"])
    response = strapi_api.delete(url)

    validate.status.no_content(response)


# ============================================================
# TC-DAU-02 - Delete author without auth token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_delete_author_missing_auth(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    url = AuthorEndpoint.delete(author["documentId"])
    response = strapi_api.delete(url, with_auth=False)

    validate.status.forbidden(response)


# ============================================================
# TC-DAU-03 - Delete author with invalid token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_delete_author_invalid_token(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    url = AuthorEndpoint.delete(author["documentId"])
    headers = {"Authorization": "Bearer INVALID123"}

    response = strapi_api.delete(url, headers=headers)

    validate.status.unauthorized(response)


# ============================================================
# TC-DAU-04 - Delete author with empty Authorization header
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_delete_author_empty_auth_header(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    url = AuthorEndpoint.delete(author["documentId"])
    headers = {"Authorization": ""}

    response = strapi_api.delete(url, headers=headers)

    validate.status.forbidden(response)


# ============================================================
# TC-DAU-05 - Delete nonexistent documentId
# BUG: Strapi returns 204 instead of 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi devuelve 204 en vez de 404 al eliminar un author inexistente", strict=False)
def test_delete_author_nonexistent(strapi_api):
    url = AuthorEndpoint.delete("aaabbbcccdddeeefff111222")

    response = strapi_api.delete(url)

    validate.status.not_found(response)


# ============================================================
# TC-DAU-06 - Delete author with empty documentId ""
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_delete_author_empty_document_id(strapi_api):
    url = AuthorEndpoint.delete("")

    response = strapi_api.delete(url)

    validate.status.method_not_allowed(response)


# ============================================================
# TC-DAU-07 - Delete author twice
# BUG: Strapi allows deleting twice instead of returning 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.bug
@pytest.mark.xfail(reason="BUG: Strapi permite eliminar dos veces el mismo author", strict=False)
def test_delete_author_twice(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    url = AuthorEndpoint.delete(author["documentId"])

    first = strapi_api.delete(url)
    validate.status.no_content(first)

    second = strapi_api.delete(url)
    validate.status.not_found(second)


# ============================================================
# TC-DAU-09 - Concurrency DELETE calls
# BUG: Strapi returns 204 for both instead of 404 on second
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi devuelve 204 en ambos DELETE concurrentes", strict=False)
def test_delete_author_concurrent(strapi_api, setup_teardown_author):
    author = setup_teardown_author
    url = AuthorEndpoint.delete(author["documentId"])

    r1 = strapi_api.delete(url)
    r2 = strapi_api.delete(url)

    validate.status.no_content(r1)
    validate.status.not_found(r2)
