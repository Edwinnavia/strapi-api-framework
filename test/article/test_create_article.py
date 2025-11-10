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
