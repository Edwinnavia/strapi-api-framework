import pytest
import time
from main.endpoints.article_endpoint import ArticleEndpoint
from main.validation_manager import ValidationManager
from data.articles import generate_article_payload

validate = ValidationManager()
pytestmark = pytest.mark.list_articles


# ============================================================
# TC-LA-01 - Consultar artículos sin filtros aplicados
# ============================================================
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_without_filters(strapi_api, module_article):
    url = ArticleEndpoint.get_all()
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'article', 'list_response_schema.json')
    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.item_field_equals(response, module_article["documentId"], "title", module_article["title"])
    validate.data.item_field_equals(response, module_article["documentId"], "slug", module_article["slug"])


# ============================================================
# TC-LA-02 - Consultar por título exacto ($eq)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_by_exact_title(strapi_api, module_article):
    params = {"filters[title][$eq]": module_article["title"]}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_count_equals(response, 1)
    validate.data.item_field_equals(response, module_article["documentId"], "title", module_article["title"])


# ============================================================
# TC-LA-03 - Título exacto sin distinción mayúsculas ($eqi)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_by_exact_title_case_insensitive(strapi_api, module_article):
    params = {"filters[title][$eqi]": module_article["title"].swapcase()}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_article["documentId"])


# ============================================================
# TC-LA-04 - Título exacto vacío ($eq="")
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_by_empty_exact_title(strapi_api):
    params = {"filters[title][$eq]": ""}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_count_equals(response, 0)


# ============================================================
# TC-LA-05 - Excluir por estado con $ne
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_by_publishedAt_not_equal(strapi_api, module_article):
    params = {"filters[publishedAt][$ne]": module_article["publishedAt"]}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_not_empty(response)
    validate.data.list_not_contains_document_id(response, module_article["documentId"])


# ============================================================
# TC-LA-06 - Condición lógica OR ($or)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_or(strapi_api, article_factory, module_article):
    second = article_factory()
    params = {
        "filters[$or][0][title][$eq]": module_article["title"],
        "filters[$or][1][slug][$eq]": second["slug"]
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.list_contains_document_id(response, second["documentId"])


# ============================================================
# TC-LA-07 - Condición lógica AND ($and)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_and(strapi_api, module_article):
    params = {
        "filters[$and][0][title][$eq]": module_article["title"],
        "filters[$and][1][slug][$eq]": module_article["slug"],
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_article["documentId"])


# ============================================================
# TC-LA-08 - ID menor que ($lt)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_id_lt(strapi_api, module_article):
    params = {"filters[id][$lt]": module_article["id"] + 1}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, module_article["documentId"])


# ============================================================
# TC-LA-09 - Rango entre ($between)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_between_single_match(strapi_api, article_factory):
    a1 = article_factory()
    time.sleep(1)
    a2 = article_factory()
    time.sleep(1)
    a3 = article_factory()

    params = {
        "filters[createdAt][$between][0]": a1["createdAt"],
        "filters[createdAt][$between][1]": a3["createdAt"],
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, a2["documentId"])


# ============================================================
# TC-LA-10 - Título contiene palabra ($contains)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_contains_title(strapi_api, article_factory):
    article = article_factory(generate_article_payload(title="PythonAutomationMagic"))
    params = {"filters[title][$contains]": "Automation"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, article["documentId"])


# ============================================================
# TC-LA-11 - Título contiene palabra sin case ($containsi)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_contains_title_case_insensitive(strapi_api, article_factory):
    article = article_factory(generate_article_payload(title="This is an automation test CASE"))
    params = {"filters[title][$containsi]": "AUTOMATION"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, article["documentId"])


# ============================================================
# TC-LA-12 - Slug inicia con ($startsWith)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_starts_with_slug(strapi_api, article_factory):
    article = article_factory(generate_article_payload(slug="automation_starts_with_this"))
    params = {"filters[slug][$startsWith]": "automation_"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, article["documentId"])
    validate.data.item_field_equals(response, article["documentId"], "slug", article["slug"])


# ============================================================
# TC-LA-13 - Slug termina con ($endsWith)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_ends_with_slug(strapi_api, article_factory):
    article = article_factory(generate_article_payload(slug="this_slug_must_end_correctly"))
    params = {"filters[slug][$endsWith]": "end_correctly"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, article["documentId"])


# ============================================================
# TC-LA-14 - Artículos publicados
# ============================================================
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_published(strapi_api, module_article):
    params = {"status": "published"}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.item_field_not_null(response, module_article["documentId"], "publishedAt")


# ============================================================
# TC-LA-15 - Artículos borrador
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_draft(strapi_api, article_factory):
    draft_payload = generate_article_payload()
    draft_payload["data"]["publishedAt"] = None

    draft = article_factory(draft_payload)
    params = {"status": "draft"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, draft["documentId"])
    validate.data.item_field_is_null(response, draft["documentId"], "publishedAt")


# ============================================================
# TC-LA-16 - Autor nulo ($null)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_author_null(strapi_api, article_factory):
    payload = generate_article_payload(author=None)
    article = article_factory(payload)

    params = {"filters[author][$null]": "true"}
    url = ArticleEndpoint.get_all(params)

    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_contains_document_id(response, article["documentId"])
    validate.data.item_field_is_null(response, article["documentId"], "author")


# ============================================================
# TC-LA-17 - Autor no nulo ($notNull)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_author_not_null(strapi_api, article_factory):
    payload = generate_article_payload(author=1)
    article = article_factory(payload)

    params = {"filters[author][$notNull]": "true", "populate": "author"}
    url = ArticleEndpoint.get_all(params)

    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.nested_field_equals(response, document_id=article["documentId"], parent_field="author",
                                      child_field="id", expected_value=1, )


# ============================================================
# TC-LA-18 - Excluir coincidencias ($not)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_not_title(strapi_api, module_article):
    params = {"filters[$not][title][$eq]": module_article["title"]}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_not_contains_document_id(response, module_article["documentId"])


# ============================================================
# TC-LA-19 - Paginación por defecto
# ============================================================
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_default_pagination(strapi_api, module_article):
    url = ArticleEndpoint.get_all()
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.pagination_value_equals(response, "page", 1)
    validate.data.pagination_value_equals(response, "pageSize", 25)


# ============================================================
# TC-LA-20 - Paginación personalizada
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_custom_pagination(strapi_api):
    params = {"pagination[page]": 2, "pagination[pageSize]": 5}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.pagination_value_equals(response, "page", 2)
    validate.data.pagination_value_equals(response, "pageSize", 5)


# ============================================================
# TC-LA-21 - withCount=false
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_without_count(strapi_api):
    params = {"pagination[withCount]": "false"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.pagination_has_keys(response, ["page", "pageSize"])
    validate.data.pagination_missing_keys(response, ["total", "pageCount"])


# ============================================================
# TC-LA-22 - Ordenado por múltiples campos
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_sorted_by_multiple_fields(strapi_api):
    params = {"sort[0]": "title:asc", "sort[1]": "createdAt:desc"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_is_sorted_by_multiple(response, [
        ("title", "asc"),
        ("createdAt", "desc"),
    ])


# ============================================================
# TC-LA-23 - Selección de campos específicos
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_select_specific_fields(strapi_api):
    params = {"fields[0]": "title", "fields[1]": "slug"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.items_only_have_fields(response, allowed_fields={"id", "documentId", "title", "slug"})
    validate.data.items_all_have_fields(response, required_fields={"title", "slug"})


# ============================================================
# TC-LA-24 - populate relaciones
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_with_populate(strapi_api, module_article):
    params = {"populate": "author"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.nested_field_equals(response, module_article["documentId"], "author", "id", 1)


# ============================================================
# TC-LA-25 - Combinación de filtros titulo + estado
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_filter_title_and_status(strapi_api, module_article):
    params = {
        "filters[title][$eq]": module_article["title"],
        "status": "published",
    }

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_count_equals(response, 1)


# ============================================================
# TC-LA-26 - Parámetros mal formateados deben ignorarse
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_list_articles_with_malformed_params_ignored(strapi_api):
    params = {"filters[title][eq]": "InvalidFormat"}  # mal formado

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)


# ============================================================
# TC-LA-27 - Tipo incorrecto en filtros
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi retorna 500 en vez de 400", strict=False)
def test_list_articles_with_invalid_filter_type(strapi_api):
    params = {"filters[id][$eq]": "not_a_number"}

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)


# ============================================================
# TC-LA-28 - Múltiples parámetros combinados
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_articles_with_multiple_params(strapi_api):
    params = {
        "status": "published",
        "sort": "title:asc",
        "pagination[pageSize]": 10,
        "populate": "author",
    }

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.data.list_not_empty(response)


# ============================================================
# TC-LA-29 - pagination[page] string
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi retorna 500 para pagination[page] texto", strict=False)
def test_pagination_page_string(strapi_api):
    params = {"pagination[page]": "text"}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)


# ============================================================
# TC-LA-30 - pagination[pageSize] string
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi retorna 500 para pagination[pageSize] texto", strict=False)
def test_pagination_page_size_string(strapi_api):
    params = {"pagination[pageSize]": "text"}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)


# ============================================================
# TC-LA-31 - pagination[page] decimal
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi permite decimal o retorna 500", strict=False)
def test_pagination_page_decimal(strapi_api):
    params = {"pagination[page]": "1.5"}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)


# ============================================================
# TC-LA-32 - pagination[pageSize] decimal
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi maneja incorrectamente pageSize decimal", strict=False)
def test_pagination_page_size_decimal(strapi_api):
    params = {"pagination[pageSize]": "10.7"}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)


# ============================================================
# TC-LA-33 - pagination[page] negativo
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi no valida números negativos en page", strict=False)
def test_pagination_page_negative(strapi_api):
    params = {"pagination[page]": "-1"}
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)
