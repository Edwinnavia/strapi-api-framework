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


# ============================================================
# TC-CA-04 - Selección de campos específicos
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_select_specific_fields(strapi_api):
    params = {"fields[0]": "name", "fields[1]": "slug"}
    url = CategoryEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.items_only_have_fields(response, allowed_fields={"id", "documentId", "name", "slug"})
    validate.data.items_all_have_fields(response, required_fields={"name", "slug"})


# ============================================================
# TC-CA-05 - Orden ascendente por nombre
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_sorted_by_name_asc(strapi_api):
    params = {"sort": "name:asc"}
    url = CategoryEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.list_is_sorted_by(response, field="name", order="asc")


# ============================================================
# TC-CA-06 - Orden descendente por fecha de creación
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_sorted_by_created_desc(strapi_api):
    params = {"sort": "createdAt:desc"}
    url = CategoryEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.list_is_sorted_by(response, field="createdAt", order="desc")


# ============================================================
# TC-CA-07 - Filtrar por nombre exacto ($eq)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_filter_exact_name(strapi_api, module_category):
    params = {"filters[name][$eq]": module_category["name"]}
    url = CategoryEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_category["documentId"])
