import pytest
from main.endpoints.category_endpoint import CategoryEndpoint
from main.validation_manager import ValidationManager
from data.categories import generate_category_payload

validate = ValidationManager()
pytestmark = pytest.mark.delete_category


# ============================================================
# TC-DC-01 - Delete category with valid documentId
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_delete_category_valid(strapi_api, setup_teardown_category):
    category = setup_teardown_category

    url = CategoryEndpoint.delete(category["documentId"])
    response = strapi_api.delete(url)

    validate.status.no_content(response)


# ============================================================
# TC-DC-02 - Delete category without auth token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_delete_category_missing_auth(strapi_api, setup_teardown_category):
    category = setup_teardown_category

    url = CategoryEndpoint.delete(category["documentId"])
    response = strapi_api.delete(url, with_auth=False)

    validate.status.forbidden(response)


# ============================================================
# TC-DC-03 - Delete category with invalid token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_delete_category_invalid_token(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.delete(category["documentId"])

    headers = {"Authorization": "Bearer INVALID123"}

    response = strapi_api.delete(url, headers=headers)

    validate.status.unauthorized(response)


# ============================================================
# TC-DC-04 - Delete category with empty Authorization header
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_delete_category_empty_auth_header(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.delete(category["documentId"])

    headers = {"Authorization": ""}

    response = strapi_api.delete(url, headers=headers)

    validate.status.forbidden(response)


# ============================================================
# TC-DC-05 - Delete nonexistent category
# BUG: Strapi returns 204 instead of 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.bug
@pytest.mark.xfail(reason="BUG: Strapi devuelve 204 en vez de 404 al eliminar categoría inexistente", strict=False)
def test_delete_category_nonexistent(strapi_api):
    url = CategoryEndpoint.delete("xxxxinvalidxxxxid123")

    response = strapi_api.delete(url)

    validate.status.not_found(response)


# ============================================================
# TC-DC-06 - Delete category with empty documentId
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_delete_category_empty_document_id(strapi_api):
    url = CategoryEndpoint.delete("")

    response = strapi_api.delete(url)

    validate.status.method_not_allowed(response)


# ============================================================
# TC-DC-07 - Delete category with invalid documentId format
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi responde 204 en vez de 404 para documentId con formato inválido", strict=False)
def test_delete_category_invalid_document_id_format(strapi_api):
    invalid_id = "@#123INVALID!!"
    url = CategoryEndpoint.delete(invalid_id)

    response = strapi_api.delete(url)

    validate.status.not_found(response)


# ============================================================
# TC-DC-08 - Delete category twice
# BUG: Strapi should return 404 on second delete
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.bug
@pytest.mark.xfail(reason="BUG: Strapi permite eliminar dos veces la misma categoría", strict=False)
def test_delete_category_twice(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.delete(category["documentId"])

    first = strapi_api.delete(url)
    validate.status.no_content(first)

    second = strapi_api.delete(url)
    validate.status.not_found(second)


# ============================================================
# TC-DC-09 - Concurrent DELETE requests
# BUG: Strapi returns 204 for both
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.bug
@pytest.mark.xfail(reason="BUG: Strapi devuelve 204 en ambos DELETE concurrentes", strict=False)
def test_delete_category_concurrent(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.delete(category["documentId"])

    r1 = strapi_api.delete(url)
    r2 = strapi_api.delete(url)

    validate.status.no_content(r1)
    validate.status.not_found(r2)
