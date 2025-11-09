import pytest
from main.endpoints.author_endpoint import AuthorEndpoint
from main.validation_manager import ValidationManager
from data.authors import generate_author_payload

validate = ValidationManager()
pytestmark = pytest.mark.list_authors


# ============================================================
# TC-AU-01 - Consultar autores sin filtros aplicados
# ============================================================
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_without_filters(strapi_api, module_author):
    url = AuthorEndpoint.get_all()
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, module_author["documentId"])
    validate.data.item_field_equals(response, module_author["documentId"], "name", module_author["name"])
    validate.data.item_field_equals(response, module_author["documentId"], "email", module_author["email"])


# ============================================================
# TC-AU-02 - Paginación por defecto
# ============================================================
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_default_pagination(strapi_api):
    url = AuthorEndpoint.get_all()
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.pagination_value_equals(response, "page", 1)
    validate.data.pagination_value_equals(response, "pageSize", 25)


# ============================================================
# TC-AU-03 - Paginación personalizada
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_custom_pagination(strapi_api):
    params = {"pagination[page]": 2, "pagination[pageSize]": 5}
    url = AuthorEndpoint.get_all(params)

    response = strapi_api.get(url)
    validate.status.ok(response)
    validate.data.pagination_value_equals(response, "page", 2)
    validate.data.pagination_value_equals(response, "pageSize", 5)
