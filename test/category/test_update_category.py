import pytest
from main.endpoints.category_endpoint import CategoryEndpoint
from main.validation_manager import ValidationManager

validate = ValidationManager()
pytestmark = pytest.mark.update_category


# ============================================================
# TC-UC-01 - Update category name with valid value
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_category_valid_name(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    payload = {"data": {"name": "Updated Category Name"}}
    response = strapi_api.put(url, payload=payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'category', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "name", "Updated Category Name")


# ============================================================
# TC-UC-02 - Update category slug with valid unique format
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_category_valid_slug(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    payload = {"data": {"slug": "updated-category-slug"}}
    response = strapi_api.put(url, payload=payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'category', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "slug", "updated-category-slug")


# ============================================================
# TC-UC-03 - Update category description valid text
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_category_valid_description(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    payload = {"data": {"description": "Updated category description"}}
    response = strapi_api.put(url, payload=payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'category', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "description", "Updated category description")


# ============================================================
# TC-UC-04 - Update multiple category fields
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_category_multiple_fields(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    payload = {
        "data": {
            "name": "Multi Name",
            "slug": "multi-slug",
            "description": "Multi description"
        }
    }

    response = strapi_api.put(url, payload=payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'category', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "name", "Multi Name")
    validate.data.item_field_equals_response(response, "slug", "multi-slug")


# ============================================================
# TC-UC-05 - Update category with valid article relations
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_category_articles_relation(strapi_api, setup_teardown_category, module_article_session):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    payload = {
        "data": {
            "articles": {
                "connect": [{"documentId": module_article_session["documentId"]}]
            }
        }
    }

    response = strapi_api.put(url, payload=payload)
    validate.status.ok(response)
    validate.schema.validate_response(response, 'category', 'update_request_schema.json')


# ============================================================
# TC-UC-06 - Update category empty description
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_category_empty_description(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    response = strapi_api.put(url, payload={"data": {"description": ""}})

    validate.status.ok(response)
    validate.schema.validate_response(response, 'category', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "description", "")


# ============================================================
# TC-UC-07 - Update a single category field
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_category_single_field(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    response = strapi_api.put(url, payload={"data": {"slug": "single-field-slug"}})

    validate.status.ok(response)
    validate.schema.validate_response(response, 'category', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "slug", "single-field-slug")


# ============================================================
# TC-UC-08 - Update category keep original slug
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_category_keep_slug(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    original_slug = category["slug"]

    url = CategoryEndpoint.update(category["documentId"])
    response = strapi_api.put(url, payload={"data": {"name": "Name Only", "slug": original_slug}})

    validate.status.ok(response)
    validate.schema.validate_response(response, 'category', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "slug", original_slug)


# ============================================================
# TC-UC-09 - Update all category fields successfully
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_category_all_fields_valid(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    payload = {
        "data": {
            "name": "Complete Update",
            "slug": "complete-update",
            "description": "Updated description"
        }
    }

    response = strapi_api.put(url, payload=payload)
    validate.status.ok(response)
    validate.schema.validate_response(response, 'category', 'update_request_schema.json')


# ============================================================
# TC-UC-10 - Update category missing authorization
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_update_category_missing_auth(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    response = strapi_api.put(url, payload={"data": {"name": "X"}}, with_auth=False)

    validate.status.forbidden(response)


# ============================================================
# TC-UC-11 - Update category invalid token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_update_category_invalid_token(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    headers = {"Authorization": "Bearer INVALIDTOKEN123"}
    response = strapi_api.put(url, payload={"data": {"name": "X"}}, headers=headers)

    validate.status.unauthorized(response)


# ============================================================
# TC-UC-12 - Update category empty name
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.xfail(reason="BUG: Strapi permite name vacío", strict=False)
def test_update_category_empty_name(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    response = strapi_api.put(url, payload={"data": {"name": ""}})
    validate.status.bad_request(response)


# ============================================================
# TC-UC-13 - Update category name too long
# BUG: Strapi retorna 500 al actualizar un nombre demasiado largo
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(
    reason="BUG: Strapi responde 500 cuando 'name' excede el límite permitido; debería devolver 400",
    strict=False
)
def test_update_category_name_too_long(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    long_name = "A" * 500

    url = CategoryEndpoint.update(category['documentId'])
    response = strapi_api.put(url, payload={"data": {"name": long_name}})

    validate.status.bad_request(response)


# ============================================================
# TC-UC-14 - Update category invalid name type
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_category_invalid_name_type(strapi_api, setup_teardown_category):
    category = setup_teardown_category

    payload = {"data": {"name": 123}}
    url = CategoryEndpoint.update(category["documentId"])

    response = strapi_api.put(url, payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-UC-15 - Update category duplicate slug
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_category_duplicate_slug(strapi_api, module_category, setup_teardown_category):
    category = setup_teardown_category

    payload = {"data": {"slug": module_category["slug"]}}
    url = CategoryEndpoint.update(category["documentId"])

    response = strapi_api.put(url, payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-UC-16 - Update category invalid slug format
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_category_invalid_slug_format(strapi_api, setup_teardown_category):
    category = setup_teardown_category
    url = CategoryEndpoint.update(category["documentId"])

    response = strapi_api.put(url, payload={"data": {"slug": "@@@@@@@"}})

    validate.status.bad_request(response)


# ============================================================
# TC-UC-17 - Update category invalid description type
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_category_invalid_description_type(strapi_api, setup_teardown_category):
    category = setup_teardown_category

    payload = {"data": {"description": {"bad": "object"}}}
    url = CategoryEndpoint.update(category["documentId"])

    response = strapi_api.put(url, payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-UC-18 - Update category with nonexistent article relations
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_category_invalid_articles(strapi_api, setup_teardown_category):
    category = setup_teardown_category

    payload = {
        "data": {
            "articles": {
                "connect": [{"documentId": "INVALIDDOCID123"}]
            }
        }
    }

    url = CategoryEndpoint.update(category["documentId"])
    response = strapi_api.put(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-UC-19 - Update category malformed JSON (missing data wrapper)
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_category_invalid_json_format(strapi_api, setup_teardown_category):
    category = setup_teardown_category

    url = CategoryEndpoint.update(category["documentId"])
    response = strapi_api.put(url, payload={"name": "Bad Format"})

    validate.status.bad_request(response)
