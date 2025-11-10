import pytest
from main.endpoints.category_endpoint import CategoryEndpoint
from main.validation_manager import ValidationManager
from data.categories import generate_category_payload

validate = ValidationManager()
pytestmark = pytest.mark.list_categories


# ============================================================
# TC-CA-01 - Consultar categorías sin filtros aplicados
# ============================================================
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_without_filters(strapi_api, module_category):
    url = CategoryEndpoint.get_all()
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.list_contains_document_id(response, module_category["documentId"])
    validate.data.item_field_equals(response, module_category["documentId"], "name", module_category["name"])


# ============================================================
# TC-CA-02 - Paginación por defecto
# ============================================================
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_default_pagination(strapi_api):
    url = CategoryEndpoint.get_all()
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.pagination_value_equals(response, "page", 1)
    validate.data.pagination_value_equals(response, "pageSize", 25)


# ============================================================
# TC-CA-03 - Paginación personalizada válida
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_custom_pagination(strapi_api):
    params = {"pagination[page]": 2, "pagination[pageSize]": 5}
    url = CategoryEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.pagination_value_equals(response, "page", 2)
    validate.data.pagination_value_equals(response, "pageSize", 5)
