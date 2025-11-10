import pytest
from main.endpoints.article_endpoint import ArticleEndpoint
from main.validation_manager import ValidationManager
from data.articles import generate_article_payload

validate = ValidationManager()
pytestmark = pytest.mark.update_article


# ============================================================
# TC-UA-01 - Actualizar título del artículo con texto válido
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_article_valid_title(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    update_payload = {"data": {"title": "Updated Title"}}

    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload=update_payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'article', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "title", "Updated Title")


# ============================================================
# TC-UA-02 - Actualizar descripción del artículo con texto válido
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_article_valid_description(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    update_payload = {"data": {"description": "New description"}}
    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload=update_payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'article', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "description", "New description")


# ============================================================
# TC-UA-03 - Actualizar slug del artículo con formato válido y único
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_article_valid_slug(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    update_payload = {"data": {"slug": "updated-slug-value"}}
    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload=update_payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'article', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "slug", "updated-slug-value")


# ============================================================
# TC-UA-04 - Actualizar varios campos del artículo (título, desc, slug)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_article_multiple_fields(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    update_payload = {
        "data": {
            "title": "Multi Update",
            "description": "Updated desc",
            "slug": "multi-update"
        }
    }

    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload=update_payload)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'article', 'update_request_schema.json')
    validate.data.item_field_equals_response(response, "title", "Multi Update")
    validate.data.item_field_equals_response(response, "slug", "multi-update")


# ============================================================
# TC-UA-05 - Actualizar artículo con solo un campo
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_article_single_field(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    url = ArticleEndpoint.update(article["documentId"])

    update_payload = {"data": {"description": "Only description updated"}}
    response = strapi_api.put(url, payload=update_payload)

    validate.status.ok(response)
    validate.data.item_field_equals_response(response, "description", "Only description updated")


# ============================================================
# TC-UA-06 - Actualizar sin cambios (data vacío)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_article_empty_data(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    url = ArticleEndpoint.update(article["documentId"])

    update_payload = {"data": {}}
    response = strapi_api.put(url, payload=update_payload)

    validate.status.ok(response)


# ============================================================
# TC-UA-07 - Mantener slug original al actualizar otros campos
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_update_article_keep_slug(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    original_slug = article["slug"]

    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload={"data": {"title": "Just title"}})

    validate.status.ok(response)
    validate.data.item_field_equals_response(response, "slug", original_slug)


# ============================================================
# TC-UA-08 - Actualizar artículo sin enviar Authorization token
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_update_article_missing_auth(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    url = ArticleEndpoint.update(article["documentId"])

    response = strapi_api.put(url, payload={"data": {"title": "X"}}, with_auth=False)

    validate.status.forbidden(response)


# ============================================================
# TC-UA-09 - Actualizar artículo con token inválido
# ============================================================
@pytest.mark.negative
@pytest.mark.security
def test_update_article_invalid_token(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    url = ArticleEndpoint.update(article["documentId"])

    headers = {"Authorization": "Bearer invalidTOKEN123"}
    response = strapi_api.put(url, payload={"data": {"title": "X"}}, headers=headers)

    validate.status.unauthorized(response)


# ============================================================
# TC-UA-10 - Actualizar título vacío ("")  BUG
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.bug
@pytest.mark.xfail(reason="BUG: Strapi permite title vacío en update", strict=False)
def test_update_article_empty_title(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    url = ArticleEndpoint.update(article["documentId"])

    update_payload = {"data": {"title": ""}}
    response = strapi_api.put(url, payload=update_payload)

    validate.status.bad_request(response)


# ============================================================
# TC-UA-11 - Actualizar título mayor a 150 caracteres  BUG
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.xfail(reason="BUG: Strapi responde 500 en vez de 400 para títulos largos", strict=False)
def test_update_article_title_too_long(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    long_title = "A" * 500

    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload={"data": {"title": long_title}})

    validate.status.bad_request(response)


# ============================================================
# TC-UA-12 - Actualizar slug con formato inválido
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_article_invalid_slug(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    update_payload = {"data": {"slug": "Invalid Slug"}}
    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload=update_payload)

    validate.status.bad_request(response)


# ============================================================
# TC-UA-13 - Actualizar slug duplicado
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_article_duplicate_slug(strapi_api, module_article, setup_teardown_article):
    article = setup_teardown_article
    duplicate_slug = module_article["slug"]

    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload={"data": {"slug": duplicate_slug}})

    validate.status.bad_request(response)


# ============================================================
# TC-UA-14 - Actualizar descripción mayor a 1000 caracteres
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_article_description_too_long(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    desc = "X" * 2000

    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload={"data": {"description": desc}})

    validate.status.bad_request(response)


# ============================================================
# TC-UA-15 - Actualizar title con tipo incorrecto (int)
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_article_invalid_title_type(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    payload = {"data": {"title": 123}}
    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-UA-16 - Actualizar description con tipo incorrecto (objeto)
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_article_invalid_description_type(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    payload = {"data": {"description": {"bad": "object"}}}
    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-UA-17 - Actualizar slug vacío
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_article_empty_slug(strapi_api, setup_teardown_article):
    article = setup_teardown_article

    payload = {"data": {"slug": ""}}
    url = ArticleEndpoint.update(article["documentId"])
    response = strapi_api.put(url, payload=payload)

    validate.status.bad_request(response)


# ============================================================
# TC-UA-18 - Actualizar con JSON mal formateado
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_article_invalid_json_format(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    url = ArticleEndpoint.update(article["documentId"])

    response = strapi_api.put(url, payload='{"data": { "title": "x" ')

    validate.status.bad_request(response)


# ============================================================
# TC-UA-19 - Actualizar con campos no reconocidos
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_update_article_unknown_field(strapi_api, setup_teardown_article):
    article = setup_teardown_article
    url = ArticleEndpoint.update(article["documentId"])

    payload = {"data": {"fakeField": "bad"}}
    response = strapi_api.put(url, payload=payload)

    validate.status.bad_request(response)
