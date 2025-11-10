import pytest
from main.endpoints.category_endpoint import CategoryEndpoint
from main.validation_manager import ValidationManager
from data.categories import generate_category_payload

validate = ValidationManager()
pytestmark = pytest.mark.get_category


# ============================================================
# TC-GC-01 - Valid documentId returns full category
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_category_valid_document_id(strapi_api, module_category):
    doc_id = module_category["documentId"]

    url = CategoryEndpoint.get_by_id(doc_id)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "detail_response_schema.json")

    validate.data.item_field_equals_response(response, "documentId", doc_id)
    validate.data.item_field_equals_response(response, "name", module_category["name"])
    validate.data.item_field_equals_response(response, "slug", module_category["slug"])


# ============================================================
# TC-GC-02 - Nonexistent documentId -> 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_category_nonexistent_document_id(strapi_api):
    invalid_id = "aaaaaaaaaaaaaaaaaaaaaaaa"

    response = strapi_api.get(CategoryEndpoint.get_by_id(invalid_id))

    validate.status.not_found(response)


# ============================================================
# TC-GC-03 - Empty documentId ""
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_category_empty_document_id(strapi_api):
    response = strapi_api.get(CategoryEndpoint.get_by_id("asdasdasdq132"))

    validate.status.not_found(response)


# ============================================================
# TC-GC-04 - Invalid documentId format
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_category_invalid_document_id_format(strapi_api):
    for invalid in ["123456", "@#$%", "cat!bad"]:
        response = strapi_api.get(CategoryEndpoint.get_by_id(invalid))
        validate.status.not_found(response)


# ============================================================
# TC-GC-05 - Validate expected fields
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_category_validate_all_fields(strapi_api, module_category):
    doc_id = module_category["documentId"]

    response = strapi_api.get(CategoryEndpoint.get_by_id(doc_id))

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "detail_response_schema.json")


# ============================================================
# TC-GC-06 - Category with empty or null description
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_category_with_empty_description(strapi_api, teardown_category):
    payload = generate_category_payload(description="")
    created = strapi_api.post(CategoryEndpoint.create(), payload=payload)

    doc_id = created.json()["data"]["documentId"]
    teardown_category.append(doc_id)

    response = strapi_api.get(CategoryEndpoint.get_by_id(doc_id))

    validate.status.ok(response)
    validate.schema.validate_response(response, "category", "detail_response_schema.json")
    validate.data.item_field_equals_response(response, "description", "")


# ============================================================
# TC-GC-07 - documentId uppercase
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_category_document_id_uppercase(strapi_api, module_category):
    invalid_id = module_category["documentId"].upper()

    response = strapi_api.get(CategoryEndpoint.get_by_id(invalid_id))

    validate.status.not_found(response)


# ============================================================
# TC-GC-08 - Deleted category returns 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_category_deleted(strapi_api):
    payload = generate_category_payload()
    created = strapi_api.post(CategoryEndpoint.create(), payload=payload)

    doc_id = created.json()["data"]["documentId"]

    strapi_api.delete(CategoryEndpoint.delete(doc_id))

    response = strapi_api.get(CategoryEndpoint.get_by_id(doc_id))

    validate.status.not_found(response)


# ============================================================
# TC-GC-09 - Multiple simultaneous GET requests
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_category_multiple_simultaneous_calls(strapi_api, teardown_category):
    payload = generate_category_payload()
    created = strapi_api.post(CategoryEndpoint.create(), payload=payload)

    doc_id = created.json()["data"]["documentId"]
    teardown_category.append(doc_id)

    url = CategoryEndpoint.get_by_id(doc_id)

    responses = [strapi_api.get(url) for _ in range(5)]

    for r in responses:
        validate.status.ok(r)
