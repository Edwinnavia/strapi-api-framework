import pytest
from main.endpoints.author_endpoint import AuthorEndpoint
from main.validation_manager import ValidationManager
from data.authors import generate_author_payload

validate = ValidationManager()
pytestmark = pytest.mark.update_author


# ============================================================
# TC-UAU-01 - Update author name with valid value
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_author_valid_name(strapi_api, setup_teardown_author):
    author = setup_teardown_author
    url = AuthorEndpoint.update(author["documentId"])

    payload = {"data": {"name": "Updated Name"}}
    response = strapi_api.put(url, payload=payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'author', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "name", "Updated Name")


# ============================================================
# TC-UAU-02 - Update author email with valid format
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_author_valid_email(strapi_api, setup_teardown_author):
    author = setup_teardown_author
    url = AuthorEndpoint.update(author["documentId"])

    payload = {"data": {"email": "updated_email@test.com"}}
    response = strapi_api.put(url, payload=payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'author', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "email", "updated_email@test.com")


# ============================================================
# TC-UAU-03 - Update author avatar with valid numeric ID
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_author_valid_avatar(strapi_api, setup_teardown_author):
    author = setup_teardown_author
    url = AuthorEndpoint.update(author["documentId"])

    payload = {"data": {"avatar": 7}}
    response = strapi_api.put(url, payload=payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'author', 'update_request_schema.json')


# ============================================================
# TC-UAU-04 - Update author with valid related articles
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_author_valid_articles_relation(strapi_api, setup_teardown_author, module_article_session):
    author = setup_teardown_author
    url = AuthorEndpoint.update(author["documentId"])

    payload = {
        "data": {
            "articles": {
                "connect": [{"documentId": module_article_session["documentId"]}]
            }
        }
    }

    response = strapi_api.put(url, payload=payload)
    validate.status.ok(response)
    validate.schema.validate_response(response, 'author', 'update_request_schema.json')


# ============================================================
# TC-UAU-05 - Update multiple author fields
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_author_multiple_fields(strapi_api, setup_teardown_author):
    author = setup_teardown_author
    url = AuthorEndpoint.update(author["documentId"])

    payload = {
        "data": {
            "name": "Multi Update",
            "email": "multi@test.com",
            "avatar": 5
        }
    }

    response = strapi_api.put(url, payload=payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'author', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "name", "Multi Update")
    validate.data.item_field_equals_response(response, "email", "multi@test.com")


# ============================================================
# TC-UAU-06 - Update a single author field
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_author_single_field(strapi_api, setup_teardown_author):
    author = setup_teardown_author
    url = AuthorEndpoint.update(author["documentId"])

    payload = {"data": {"name": "Only Name Updated"}}
    response = strapi_api.put(url, payload=payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'author', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "name", "Only Name Updated")


# ============================================================
# TC-UAU-07 - Update author without modifying email
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_author_keep_email(strapi_api, setup_teardown_author):
    author = setup_teardown_author
    original_email = author["email"]

    url = AuthorEndpoint.update(author["documentId"])
    response = strapi_api.put(url, payload={"data": {"name": "Updated Only Name"}})

    validate.status.ok(response)
    validate.schema.validate_response(response, 'author', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "email", original_email)


# ============================================================
# TC-UAU-08 - Update author name with special characters
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_author_special_characters_name(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    payload = {"data": {"name": "José Niño Álvarez"}}
    url = AuthorEndpoint.update(author["documentId"])

    response = strapi_api.put(url, payload=payload)
    validate.status.ok(response)
    validate.schema.validate_response(response, 'author', 'update_request_schema.json')


# ============================================================
# TC-UAU-09 - Update author avatar to null
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_author_avatar_null(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    payload = {"data": {"avatar": None}}
    url = AuthorEndpoint.update(author["documentId"])

    response = strapi_api.put(url, payload=payload)
    validate.status.ok(response)
    validate.schema.validate_response(response, 'author', 'update_request_schema.json')


# ============================================================
# TC-UAU-10 - Update author missing auth token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_update_author_missing_auth(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    url = AuthorEndpoint.update(author["documentId"])
    response = strapi_api.put(url, payload={"data": {"name": "X"}}, with_auth=False)

    validate.status.forbidden(response)


# ============================================================
# TC-UAU-11 - Update author invalid token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_update_author_invalid_token(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    url = AuthorEndpoint.update(author["documentId"])
    headers = {"Authorization": "Bearer INVALIDTOKEN123"}

    response = strapi_api.put(url, payload={"data": {"name": "X"}}, headers=headers)

    validate.status.unauthorized(response)


# ============================================================
# TC-UAU-12 - Update author empty name
# BUG: Strapi accepts empty names
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi acepta name vacío en update", strict=False)
def test_update_author_empty_name(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    payload = {"data": {"name": ""}}
    url = AuthorEndpoint.update(author["documentId"])

    response = strapi_api.put(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-UAU-13 - Update author name too long
# BUG: Strapi responde 500 cuando name excede el máximo permitido
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(
    reason="BUG: Strapi retorna 500 al actualizar author.name demasiado largo; debería retornar 400",
    strict=False
)
def test_update_author_name_too_long(strapi_api, setup_teardown_author):
    author = setup_teardown_author
    url = AuthorEndpoint.update(author["documentId"])

    long_name = "A" * 500
    response = strapi_api.put(url, payload={"data": {"name": long_name}})

    validate.status.bad_request(response)


# ============================================================
# TC-UAU-14 - Update author invalid name type (int)
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_author_invalid_name_type(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    payload = {"data": {"name": 123}}
    url = AuthorEndpoint.update(author["documentId"])

    response = strapi_api.put(url, payload=payload)

    validate.status.bad_request(response)

# ============================================================
# TC-UAU-15 - Update author invalid email format
# BUG: Strapi permite email inválido y responde 200 en lugar de 400
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(
    reason="BUG: Strapi permite actualizar un email sin formato válido (ej. 'test') y devuelve 200; debería devolver 400",
    strict=False
)
def test_update_author_invalid_email_format(strapi_api, setup_teardown_author):
    author = setup_teardown_author
    url = AuthorEndpoint.update(author["documentId"])

    payload = {"data": {"email": "test"}}
    response = strapi_api.put(url, payload=payload)

    validate.status.bad_request(response)



# ============================================================
# TC-UAU-16 - Update author avatar negative ID
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_author_negative_avatar(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    payload = {"data": {"avatar": -5}}
    url = AuthorEndpoint.update(author["documentId"])

    response = strapi_api.put(url, payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-UAU-17 - Update author avatar wrong type
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_author_avatar_wrong_type(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    payload = {"data": {"avatar": "7a"}}
    url = AuthorEndpoint.update(author["documentId"])

    response = strapi_api.put(url, payload=payload)
    validate.status.bad_request(response)


# ============================================================
# TC-UAU-18 - Update author with nonexistent article documentId
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_author_invalid_articles(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    payload = {
        "data": {
            "articles": {
                "connect": [{"documentId": "INVALID123IDXYZ"}]
            }
        }
    }

    url = AuthorEndpoint.update(author["documentId"])
    response = strapi_api.put(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-UAU-19 - Update author with empty articles connect
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_author_articles_empty_array(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    payload = {"data": {"articles": {"connect": []}}}
    url = AuthorEndpoint.update(author["documentId"])

    response = strapi_api.put(url, payload=payload)
    validate.status.ok(response)


# ============================================================
# TC-UAU-20 - Update author invalid JSON format (missing data)
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_author_invalid_json_format(strapi_api, setup_teardown_author):
    author = setup_teardown_author

    url = AuthorEndpoint.update(author["documentId"])
    response = strapi_api.put(url, payload={"name": "Bad Format"})

    validate.status.bad_request(response)
