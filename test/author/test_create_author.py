import pytest
from main.endpoints.author_endpoint import AuthorEndpoint
from main.validation_manager import ValidationManager
from data.authors import generate_author_payload

validate = ValidationManager()
pytestmark = pytest.mark.create_author


# ============================================================
# TC-CAU-01 - Create author with all valid fields
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_all_valid_fields(strapi_api, teardown_author, module_article_session):
    payload = generate_author_payload(
        name="Pedro Alvarez",
        email="pedro@example.com",
        articles=[module_article_session["documentId"]],
        avatar=7
    )

    validate.schema.validate_payload(payload, "author", "create_request_schema.json")

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_author.append(data["documentId"])
    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")
    validate.data.item_field_equals_response(response, "name", "Pedro Alvarez")


# ============================================================
# TC-CAU-02 - Create author with required fields only
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_minimum_fields(strapi_api, teardown_author):
    payload = generate_author_payload()

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_author.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")


# ============================================================
# TC-CAU-03 - Name within valid length range
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_valid_name_length(strapi_api, teardown_author):
    name = "A" * 100
    payload = generate_author_payload(name=name)

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_author.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")
    validate.data.item_field_equals_response(response, "name", name)


# ============================================================
# TC-CAU-04 - Create author with valid email
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_valid_email(strapi_api, teardown_author):
    payload = generate_author_payload(email="valid@mail.com")

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_author.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")


# ============================================================
# TC-CAU-05 - Create author with valid article relation
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_with_valid_article_relation(strapi_api, teardown_author, module_article_session):
    payload = generate_author_payload(articles=[module_article_session["documentId"]])

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_author.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")


# ============================================================
# TC-CAU-06 - Create author with valid avatar
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_with_valid_avatar(strapi_api, teardown_author):
    payload = generate_author_payload(avatar=7)

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_author.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")


# ============================================================
# TC-CAU-07 - Create author with accented characters
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_name_with_special_chars(strapi_api, teardown_author):
    payload = generate_author_payload(name="José Núñez Álvarez")

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_author.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")


# ============================================================
# TC-CAU-08 - Case-insensitive email
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_lowercase_email(strapi_api, teardown_author):
    payload = generate_author_payload(email="lowercase@mail.com")

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    teardown_author.append(response.json()["data"]["documentId"])
    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")


# ============================================================
# TC-CAU-09 - Create author without articles
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_without_articles(strapi_api, teardown_author):
    payload = generate_author_payload(articles=None)

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    teardown_author.append(response.json()["data"]["documentId"])
    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")


# ============================================================
# TC-CAU-10 - Create author with empty articles.connect list
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_create_author_empty_articles_connect(strapi_api, teardown_author):
    payload = generate_author_payload(articles=[])

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)

    data = response.json()["data"]
    teardown_author.append(data["documentId"])

    validate.status.created(response)
    validate.schema.validate_response(response, "author", "create_response_schema.json")


# ============================================================
# TC-CAU-11 - Missing required name
# BUG: Strapi permite crear un autor con name=None en lugar de retornar 400
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi permite crear un author con name=None en vez de retornar 400", strict=False)
def test_create_author_missing_name(strapi_api, teardown_author):
    payload = generate_author_payload()
    payload["data"]["name"] = None

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass

    validate.status.bad_request(response)


# ============================================================
# TC-CAU-12 - Empty name ""
# BUG: Strapi permite crear un author con name="" en lugar de retornar 400
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi acepta name='' en vez de validar como campo requerido", strict=False)
def test_create_author_empty_name(strapi_api, teardown_author):
    payload = generate_author_payload(name="")
    payload["data"]["name"] = ""

    url = AuthorEndpoint.create()
    response = strapi_api.post(url, payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.bad_request(response)


# ============================================================
# TC-CAU-13 - Numeric name
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_author_numeric_name(strapi_api, teardown_author):
    payload = generate_author_payload()
    payload["data"]["name"] = 123
    response = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.bad_request(response)


# ============================================================
# TC-CAU-14 - Name exceeds max length
# BUG: Strapi retorna 500 en vez de 400 cuando name supera el límite permitido
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi responde 500 para name demasiado largo, debería retornar 400", strict=False)
def test_create_author_name_too_long(strapi_api, teardown_author):
    payload = generate_author_payload(name="A" * 500)

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.bad_request(response)


# ============================================================
# TC-CAU-15 - Missing email field
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_author_missing_email(strapi_api, teardown_author):
    payload = generate_author_payload()
    payload["data"]["email"] = None

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.created(response)


# ============================================================
# TC-CAU-16 - Empty email ""
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_author_empty_email(strapi_api, teardown_author):
    payload = generate_author_payload(email="")

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.created(response)


# ============================================================
# TC-CAU-17 - Invalid email format
# BUG: Strapi no valida el formato del email y permite valores inválidos
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi acepta email inválido 'bademail' en vez de retornar 400", strict=False)
def test_create_author_invalid_email_format(strapi_api, teardown_author):
    payload = generate_author_payload(email="bademail")

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.bad_request(response)


# ============================================================
# TC-CAU-18 - Invalid article documentId
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_author_invalid_article_relation(strapi_api, teardown_author):
    payload = generate_author_payload(articles=["nonExisting123"])

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.bad_request(response)


# ============================================================
# TC-CAU-19 - Negative avatar ID
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_author_negative_avatar(strapi_api, teardown_author):
    payload = generate_author_payload(avatar=-10)

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.bad_request(response)


# ============================================================
# TC-CAU-20 - Avatar as string
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_author_string_avatar(strapi_api, teardown_author):
    payload = generate_author_payload(avatar="lol")

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.bad_request(response)


# ============================================================
# TC-CAU-21 - Missing auth token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_create_author_missing_auth(strapi_api, teardown_author):
    payload = generate_author_payload()

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload, with_auth=False)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.forbidden(response)


# ============================================================
# TC-CAU-22 - Invalid auth token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_create_author_invalid_token(strapi_api, teardown_author):
    payload = generate_author_payload()
    headers = {"Authorization": "Bearer INVALID123"}

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload, headers=headers)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.unauthorized(response)


# ============================================================
# TC-CAU-23 - Missing 'data' wrapper
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_create_author_invalid_body_format(strapi_api, teardown_author):
    payload = {"name": "Bad format"}

    response = strapi_api.post(AuthorEndpoint.create(), payload=payload)
    try:
        data = response.json().get("data")
        if data and isinstance(data, dict):
            author_id = data.get("documentId") or data.get("id")
            if author_id:
                teardown_author.append(author_id)
    except Exception:
        pass
    validate.status.bad_request(response)
