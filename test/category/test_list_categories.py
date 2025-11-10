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

