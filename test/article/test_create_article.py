import pytest
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


# ============================================================
# TC-CA-04 - Create article with valid author and category
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_article_with_author_and_category(strapi_api, teardown_article, module_author_session,
                                                 module_category_session):
    payload = generate_article_payload(author=module_author_session["id"], category=module_category_session["id"])
    validate.schema.validate_payload(payload, "article", "create_request_schema.json")

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)
    data = response.json()["data"]
    teardown_article.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "article", "create_response_schema.json")


# ============================================================
# TC-CA-06 - Create article with valid slug format
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_article_slug_format(strapi_api, teardown_article):
    payload = generate_article_payload(slug="valid-slug-format")
    validate.schema.validate_payload(payload, "article", "create_request_schema.json")

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)
    data = response.json()["data"]

    teardown_article.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "article", "create_response_schema.json")
    validate.data.item_field_equals_response(response, "slug", "valid-slug-format")


# ============================================================
# TC-CA-07 - Create article with valid title length
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_article_valid_title_length(strapi_api, teardown_article):
    title = "A" * 150
    payload = generate_article_payload(title=title)

    validate.schema.validate_payload(payload, "article", "create_request_schema.json")

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)
    data = response.json()["data"]

    teardown_article.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "article", "create_response_schema.json")
    validate.data.item_field_equals_response(response, "title", title)


# ============================================================
# TC-CA-08 - Create article with description exceeding max length
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_article_description_exceeds_max_length(strapi_api, teardown_article):
    description = "D" * 1001
    payload = generate_article_payload(description=description)

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-CA-9 - Create article with single category connected
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_article_single_category(strapi_api, teardown_article, module_category_session):
    payload = generate_article_payload(category=module_category_session["id"])
    validate.schema.validate_payload(payload, "article", "create_request_schema.json")

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_article.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "article", "create_response_schema.json")


# ============================================================
# TC-CA-10 - Missing required title field
# BUG: Strapi permite crear artículos sin título
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi no valida el campo title como requerido", strict=False)
def test_create_article_missing_title(strapi_api):
    payload = generate_article_payload()
    payload["data"]["title"] = None

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-CA-11 - Title is numeric instead of string
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_article_numeric_title(strapi_api):
    payload = generate_article_payload(title=132)
    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-CA-12 - Title exceeds maximum allowed length
# BUG: Strapi retorna 500 en vez de 400 cuando title supera el límite
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi retorna 500 en vez de 400 cuando title es demasiado largo", strict=False)
def test_create_article_title_too_long(strapi_api):
    long_title = "A" * 500
    payload = generate_article_payload(title=long_title)

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-CA-13 - Duplicate slug should return conflict
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_article_duplicate_slug(strapi_api, module_article):
    payload = generate_article_payload(slug=module_article["slug"])

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-CA-14 - Invalid slug format (spaces / uppercase)
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_article_invalid_slug_format(strapi_api):
    payload = generate_article_payload(slug="Invalid Slug Format")

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-CA-15 - Invalid description type (object)
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_article_invalid_description_type(strapi_api):
    payload = generate_article_payload(description={"invalid": "object"})

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-CA-16 - Nonexistent author id
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_article_invalid_author(strapi_api):
    payload = generate_article_payload(author=9999999)

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-CA-17 - Nonexistent category id
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_article_invalid_category(strapi_api):
    payload = generate_article_payload(category=9999999)

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-CA-18 - Missing authorization token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_create_article_missing_auth_token(strapi_api):
    payload = generate_article_payload()

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload, with_auth=False)

    validate.status.forbidden(response)


# ============================================================
# TC-CA-19 - Invalid authorization token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_create_article_invalid_token(strapi_api):
    payload = generate_article_payload()

    headers = {"Authorization": "Bearer INVALIDTOKEN123"}

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload, headers=headers)

    validate.status.unauthorized(response)


# ============================================================
# TC-CA-20 - Empty body should fail
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_article_empty_body(strapi_api):
    payload = {}

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-CA-21 - Body missing "data" wrapper
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_article_invalid_body_format(strapi_api):
    payload = {"title": "Bad format, missing data object"}

    url = ArticleEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    validate.status.bad_request(response)
