import pytest
import time
from main.endpoints.article_endpoint import ArticleEndpoint
from main.validation_manager import ValidationManager
from data.articles import generate_article_payload

validate = ValidationManager()
pytestmark = pytest.mark.create_article


# ============================================================
# TC-CA-01 - Create article with all valid fields
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_article_all_valid_fields(strapi_api, teardown_article):
    payload = generate_article_payload()
    validate.schema.validate_payload(payload, "article", "create_request_schema.json")
    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)
    teardown_article.append(response.json()["data"]["documentId"])
    validate.status.created(response)
    validate.schema.validate_response(response, "article", "create_response_schema.json")

    validate.data.item_field_equals_response(response, "title", payload["data"]["title"])
    validate.data.item_field_equals_response(response, "slug", payload["data"]["slug"])


# ============================================================
# TC-CA-02 - Create article with minimum required fields
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_article_minimum_fields(strapi_api, teardown_article):
    payload = generate_article_payload(title="My First Article")
    validate.schema.validate_payload(payload, "article", "create_request_schema.json")

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    teardown_article.append(response.json()["data"]["documentId"])
    validate.status.created(response)
    validate.schema.validate_response(response, "article", "create_response_schema.json")
    validate.data.item_field_equals_response(response, "title", payload["data"]["title"])


# ============================================================
# TC-CA-03 - Create article with empty description
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_article_empty_description(strapi_api, teardown_article):
    payload = generate_article_payload(description="")
    validate.schema.validate_payload(payload, "article", "create_request_schema.json")
    url = ArticleEndpoint.create()

    response = strapi_api.post(url, payload=payload)
    teardown_article.append(response.json()["data"]["documentId"])

    validate.status.created(response)


# ============================================================
# TC-CA-04 - Create article as draft (publishedAt null)
# BUG: Strapi incorrectly publishes articles with publishedAt=None
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.bug
@pytest.mark.xfail(reason="BUG: Strapi publica artículos aunque publishedAt=None y status='draft'", strict=False)
def test_create_article_draft_with_null_publishedAt(strapi_api, teardown_article):
    payload = generate_article_payload()
    payload["data"]["publishedAt"] = None
    payload["status"] = "draft"

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_article.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "article", "create_response_schema.json")

    list_params = {"status": "published"}
    list_url = ArticleEndpoint.get_all(list_params)
    list_response = strapi_api.get(list_url)

    validate.status.ok(list_response)
    validate.data.list_not_contains_document_id(list_response, data["documentId"])
