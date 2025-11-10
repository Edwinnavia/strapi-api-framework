import pytest
from main.endpoints.article_endpoint import ArticleEndpoint
from main.validation_manager import ValidationManager
from data.articles import generate_article_payload

validate = ValidationManager()
pytestmark = pytest.mark.get_article


# ============================================================
# TC-GA-01 - Valid documentId returns full article
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_article_valid_document_id(strapi_api, module_article):
    doc_id = module_article["documentId"]

    url = ArticleEndpoint.get_by_id(doc_id)
    response = strapi_api.get(url)
    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "detail_response_schema.json")
    validate.data.item_field_equals_response(response, "documentId", doc_id)
    validate.data.item_field_equals_response(response, "slug", module_article["slug"])
    validate.data.item_field_equals_response(response, "title", module_article["title"])


# ============================================================
# TC-GA-02 - Nonexistent documentId should return 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_article_nonexistent_document_id(strapi_api):
    invalid_id = "aaaaaaaaaaaaaaaaaaaaaaaa"
    url = ArticleEndpoint.get_by_id(invalid_id)

    response = strapi_api.get(url)

    validate.status.not_found(response)


# ============================================================
# TC-GA-03 - Invalid documentId format
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_article_invalid_format_document_id(strapi_api):
    invalid_id = "12345asa132"
    url = ArticleEndpoint.get_by_id(invalid_id)

    response = strapi_api.get(url)

    validate.status.not_found(response)


# ============================================================
# TC-GA-04 - Null fields in article should still return 200
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_article_with_null_fields(strapi_api, teardown_article):
    payload = generate_article_payload(title="", description="", slug="")
    payload["data"]["description"] = ""
    created = strapi_api.post(ArticleEndpoint.create(), payload=payload)
    doc_id = created.json()["data"]["documentId"]
    teardown_article.append(doc_id)

    url = ArticleEndpoint.get_by_id(doc_id)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "detail_response_schema.json")
    validate.data.item_field_equals_response(response, "description", "")


# ============================================================
# TC-GA-05 - Validate expected keys in response
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_article_validate_all_fields(strapi_api, module_article):
    doc_id = module_article["documentId"]

    url = ArticleEndpoint.get_by_id(doc_id)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "detail_response_schema.json")


# ============================================================
# TC-GA-06 - documentId uppercase (case-sensitive)
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_article_document_id_uppercase(strapi_api, module_article):
    invalid_id = module_article["documentId"].upper()
    url = ArticleEndpoint.get_by_id(invalid_id)

    response = strapi_api.get(url)

    validate.status.not_found(response)


# ============================================================
# TC-GA-07 - documentId with special characters
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_article_document_id_special_chars(strapi_api):
    invalid_id = "@#$%INVALIDID"
    url = ArticleEndpoint.get_by_id(invalid_id)

    response = strapi_api.get(url)

    validate.status.not_found(response)


# ============================================================
# TC-GA-08 - Access deleted article should 404
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_get_article_deleted(strapi_api):
    payload = generate_article_payload()
    created = strapi_api.post(ArticleEndpoint.create(), payload=payload)

    doc_id = created.json()["data"]["documentId"]

    strapi_api.delete(ArticleEndpoint.delete(doc_id))

    url = ArticleEndpoint.get_by_id(doc_id)
    response = strapi_api.get(url)

    validate.status.not_found(response)


# ============================================================
# TC-GA-09 - Multiple parallel GET calls
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_get_article_multiple_simultaneous_calls(strapi_api, teardown_article):
    payload = generate_article_payload()
    created = strapi_api.post(ArticleEndpoint.create(), payload=payload)

    doc_id = created.json()["data"]["documentId"]
    teardown_article.append(doc_id)

    url = ArticleEndpoint.get_by_id(doc_id)

    responses = [strapi_api.get(url) for _ in range(5)]

    for r in responses:
        validate.status.ok(r)
