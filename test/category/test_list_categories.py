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
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_category["documentId"])


# ============================================================
# TC-CA-08 - Nombre contiene parcial ($contains)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_filter_contains_name(strapi_api, module_category):
    fragment = module_category["name"][:3]
    params = {"filters[name][$contains]": fragment}
    url = CategoryEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.list_contains_document_id(response, module_category["documentId"])


# ============================================================
# TC-CA-09 - Description nula ($null)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_filter_description_null(strapi_api, category_factory):
    payload = generate_category_payload(description=None)
    category = category_factory(payload)

    params = {"filters[description][$null]": "true"}
    url = CategoryEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.item_field_is_null(response, category["documentId"], "description")


# ============================================================
# TC-CA-10 - Description no nula ($notNull)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_filter_description_not_null(strapi_api, category_factory):
    payload = generate_category_payload(description="Some text")
    category = category_factory(payload)

    params = {"filters[description][$notNull]": "true"}
    url = CategoryEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.item_field_equals(response, category["documentId"], "description", "Some text")


# ============================================================
# TC-CA-11 - Filtros múltiples (name + slug)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_categories_filter_name_and_slug(strapi_api, module_category):
    params = {
        "filters[name][$eq]": module_category["name"],
        "filters[slug][$eq]": module_category["slug"],
    }
    url = CategoryEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
