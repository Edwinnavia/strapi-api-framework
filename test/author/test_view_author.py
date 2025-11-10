import pytest
from main.endpoints.author_endpoint import AuthorEndpoint
from main.validation_manager import ValidationManager
from data.authors import generate_author_payload

validate = ValidationManager()
pytestmark = pytest.mark.get_author


# ============================================================
# TC-GAU-01 - Valid documentId returns full author
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_author_valid_document_id(strapi_api, module_author):
    doc_id = module_author["documentId"]

    url = AuthorEndpoint.get_by_id(doc_id)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "detail_response_schema.json")

    validate.data.item_field_equals_response(response, "documentId", doc_id)
    validate.data.item_field_equals_response(response, "name", module_author["name"])
    validate.data.item_field_equals_response(response, "email", module_author["email"])


# ============================================================
# TC-GAU-02 - Nonexistent documentId should return 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_author_nonexistent_document_id(strapi_api):
    invalid_id = "aaaaaaaaaaaaaaaaaaaaaaaa"

    response = strapi_api.get(AuthorEndpoint.get_by_id(invalid_id))

    validate.status.not_found(response)


# ============================================================
# TC-GAU-03 - Empty documentId ""
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_author_empty_document_id(strapi_api):
    response = strapi_api.get(AuthorEndpoint.get_by_id("12345asa132"))

    validate.status.not_found(response)


# ============================================================
# TC-GAU-04 - Invalid documentId format
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_author_invalid_document_id_format(strapi_api):
    for invalid in ["123456", "@#$%", "id!invalid"]:
        response = strapi_api.get(AuthorEndpoint.get_by_id(invalid))
        validate.status.not_found(response)


# ============================================================
# TC-GAU-05 - Populate avatar
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_author_with_populate_avatar(strapi_api, module_author):
    doc_id = module_author["documentId"]

    url = AuthorEndpoint.get_by_id(doc_id)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "detail_response_schema.json")


# ============================================================
# TC-GAU-06 - Validate all expected fields
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_author_validate_all_fields(strapi_api, module_author):
    doc_id = module_author["documentId"]

    response = strapi_api.get(AuthorEndpoint.get_by_id(doc_id))

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "detail_response_schema.json")


# ============================================================
# TC-GAU-07 - Avatar is null or empty
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_author_avatar_null(strapi_api, teardown_author):
    payload = generate_author_payload(avatar=None)

    created = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    doc_id = created.json()["data"]["documentId"]
    teardown_author.append(doc_id)

    response = strapi_api.get(AuthorEndpoint.get_by_id(doc_id))

    validate.status.ok(response)
    validate.data.item_field_is_null_response(response, "avatar")


# ============================================================
# TC-GAU-08 - documentId uppercase
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_author_document_id_uppercase(strapi_api, module_author):
    invalid_id = module_author["documentId"].upper()

    response = strapi_api.get(AuthorEndpoint.get_by_id(invalid_id))

    validate.status.not_found(response)


# ============================================================
# TC-GAU-09 - Access deleted author returns 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_author_deleted(strapi_api):
    payload = generate_author_payload()
    created = strapi_api.post(AuthorEndpoint.create(), payload=payload)

    doc_id = created.json()["data"]["documentId"]
    strapi_api.delete(AuthorEndpoint.delete(doc_id))

    response = strapi_api.get(AuthorEndpoint.get_by_id(doc_id))

    validate.status.not_found(response)


# ============================================================
# TC-GAU-10 - Multiple simultaneous GET requests
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_author_multiple_simultaneous_calls(strapi_api, teardown_author):
    payload = generate_author_payload()
    created = strapi_api.post(AuthorEndpoint.create(), payload=payload)

    doc_id = created.json()["data"]["documentId"]
    teardown_author.append(doc_id)

    url = AuthorEndpoint.get_by_id(doc_id)

    responses = [strapi_api.get(url) for _ in range(5)]

    for r in responses:
        validate.status.ok(r)
