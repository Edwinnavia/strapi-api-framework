import pytest
from main.endpoints.category_endpoint import CategoryEndpoint
from main.validation_manager import ValidationManager
from data.categories import generate_category_payload

validate = ValidationManager()
pytestmark = pytest.mark.create_category


# ============================================================
# TC-LC-01 - Create category with all valid fields
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_category_all_valid_fields(strapi_api, teardown_category, module_article_session):
    payload = generate_category_payload(
        name="Tecnología",
        slug="tecnologia",
        description="Categoría de artículos técnicos"
    )

    validate.schema.validate_payload(payload, "category", "create_request_schema.json")

    url = CategoryEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_category.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "category", "create_response_schema.json")
    validate.data.item_field_equals_response(response, "slug", "tecnologia")


# ============================================================
# TC-LC-02 - Create category with minimum required fields
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_category_minimum_fields(strapi_api, teardown_category):
    payload = generate_category_payload(description=None, articles=None)

    url = CategoryEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_category.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "category", "create_response_schema.json")


# ============================================================
# TC-LC-03 - Create category with min name length
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_category_min_name_length(strapi_api, teardown_category):
    payload = generate_category_payload(name="A")

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    teardown_category.append(response.json()["data"]["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "category", "create_response_schema.json")


# ============================================================
# TC-LC-04 - Name exceeds maximum allowed length
# BUG: Strapi devuelve 500 en vez de 400 para nombre demasiado largo
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi responde 500 cuando name > límite; debería retornar 400", strict=False)
def test_create_category_name_too_long(strapi_api):
    name = "A" * 500
    payload = generate_category_payload(name=name)

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-LC-05 - Valid slug
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_category_valid_slug(strapi_api, teardown_category):
    payload = generate_category_payload(slug="categoria-slug-valido")

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    teardown_category.append(response.json()["data"]["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "category", "create_response_schema.json")
    validate.data.item_field_equals_response(response, "slug", "categoria-slug-valido")


# ============================================================
# TC-LC-06 - Valid description length
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_category_valid_description(strapi_api, teardown_category):
    desc = "A" * 300
    payload = generate_category_payload(description=desc)

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    teardown_category.append(response.json()["data"]["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "category", "create_response_schema.json")


# ============================================================
# TC-LC-07 - Category without description
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_category_without_description(strapi_api, teardown_category):
    payload = generate_category_payload(description=None)

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    teardown_category.append(response.json()["data"]["documentId"])

    validate.status.created(response)


# ============================================================
# TC-LC-08 - Category with valid article relation
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_category_with_valid_articles(strapi_api, teardown_category, module_article_session):
    payload = generate_category_payload(articles=[module_article_session["documentId"]])

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    teardown_category.append(response.json()["data"]["documentId"])

    validate.status.created(response)


# ============================================================
# TC-LC-09 - Special chars in name
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_category_name_special_chars(strapi_api, teardown_category):
    payload = generate_category_payload(name="Categoría Ñá")

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-LC-10 - Unique name and slug
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_category_unique_fields(strapi_api, teardown_category):
    payload = generate_category_payload(name="Categoria Unica", slug="categoria-unica")

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    teardown_category.append(response.json()["data"]["documentId"])

    validate.status.created(response)


# ============================================================
# TC-LC-11 - Missing required name
# BUG: Strapi permite crear categoría sin nombre en lugar de retornar 400
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi crea categoría cuando 'name'=None; debería retornar 400", strict=False)
def test_create_category_missing_name(strapi_api):
    payload = generate_category_payload()
    payload["data"]["name"] = None

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-LC-12 - Empty name ""
# BUG: Strapi permite crear categoría con name vacío en lugar de retornar 400
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi acepta name="" y crea la categoría; debería retornar 400", strict=False)
def test_create_category_empty_name(strapi_api):
    payload = generate_category_payload(name="")  # name vacío

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-LC-13 - Numeric name
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_category_numeric_name(strapi_api):
    payload = generate_category_payload(name=123)

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-LC-14 - Name too long
# BUG: Strapi responde 500 cuando el nombre excede el máximo permitido
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(
    reason="BUG: Strapi retorna 500 cuando name > límite; debería retornar 400",
    strict=False
)
def test_create_category_name_too_long(strapi_api):
    payload = generate_category_payload(name="A" * 500)

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-LC-15 - Missing slug
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_category_missing_slug(strapi_api):
    payload = generate_category_payload()
    payload["data"]["slug"] = None

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    validate.status.created(response)


# ============================================================
# TC-LC-16 - Duplicate slug
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_category_duplicate_slug(strapi_api, module_category_session):
    payload = generate_category_payload(slug=module_category_session["slug"])

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-LC-17 - Invalid slug with accents/spaces
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_category_invalid_slug_accents(strapi_api):
    payload = generate_category_payload(slug="Categoría Tecnología")

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-LC-18 - Invalid description type
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_category_invalid_description_type(strapi_api):
    payload = generate_category_payload(description={"invalid": True})

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-LC-19 - Empty articles.connect
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_category_empty_articles_connect(strapi_api):
    payload = {"data": {"name": "AAA", "slug": "aaa", "articles": {"connect": []}}}

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    validate.status.created(response)


# ============================================================
# TC-LC-20 - Invalid connect object {}
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_category_invalid_connect_object(strapi_api):
    payload = {"data": {"name": "AAA", "slug": "aaa", "articles": {"connect": [{}]}}}

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-LC-21 - Invalid connect null
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_category_connect_null(strapi_api):
    payload = {"data": {"name": "AAA", "slug": "aaa", "articles": {"connect": [None]}}}

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-LC-22 - Invalid body format
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_category_invalid_body_format(strapi_api):
    payload = {"name": "No Wrapper", "slug": "no-wrapper"}

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-LC-23 - Missing or invalid token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_create_category_missing_token(strapi_api):
    payload = generate_category_payload()

    response = strapi_api.post(CategoryEndpoint.create(), payload=payload, with_auth=False)
    validate.status.forbidden(response)
