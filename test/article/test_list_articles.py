from main.endpoints.article_endpoint import ArticleEndpoint
from main.validation_manager import ValidationManager
from data.articles import generate_article_payload
import time

validate = ValidationManager()


def test_list_articles_without_filters(strapi_api, module_article):
    url = ArticleEndpoint.get_all()
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, 'article', 'list_response_schema.json')
    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.item_field_equals(response, module_article["documentId"], "title", module_article["title"])
    validate.data.item_field_equals(response, module_article["documentId"], "slug", module_article["slug"])


def test_list_articles_filter_by_exact_title(strapi_api, module_article):
    params = {
        "filters[title][$eq]": module_article["title"]
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.item_field_equals(response, module_article["documentId"], "title", module_article["title"])


def test_list_articles_filter_by_exact_title_case_insensitive(strapi_api, module_article):
    params = {
        "filters[title][$eqi]": module_article["title"].swapcase()
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_article["documentId"])


def test_list_articles_filter_by_empty_exact_title(strapi_api):
    params = {
        "filters[title][$eq]": ""
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_count_equals(response, 0)


def test_list_articles_filter_by_publishedAt_not_equal(strapi_api, module_article):
    params = {
        "filters[publishedAt][$ne]": module_article["publishedAt"]
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_not_empty(response)
    validate.data.list_not_contains_document_id(response, module_article["documentId"])


def test_list_articles_filter_or(strapi_api, article_factory, module_article):
    second_article = article_factory()
    params = {
        "filters[$or][0][title][$eq]": module_article["title"],
        "filters[$or][1][slug][$eq]": second_article["slug"]
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.list_contains_document_id(response, second_article["documentId"])


def test_list_articles_filter_and(strapi_api, module_article):
    params = {
        "filters[$and][0][title][$eq]": module_article["title"],
        "filters[$and][1][slug][$eq]": module_article["slug"],
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_article["documentId"])


def test_list_articles_filter_id_lt(strapi_api, module_article):
    params = {
        "filters[id][$lt]": module_article["id"] + 1
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.item_field_equals(response, module_article["documentId"], "id", module_article["id"])


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
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_contains_document_id(response, a2["documentId"])


def test_list_articles_filter_contains_title(strapi_api, article_factory):
    article = article_factory(
        generate_article_payload(title="PythonAutomationMagic")
    )
    params = {
        "filters[title][$contains]": "Automation"
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_contains_document_id(response, article["documentId"])


def test_list_articles_filter_contains_title_case_insensitive(strapi_api, article_factory):
    article = article_factory(
        generate_article_payload(title="This is an automation test CASE")
    )
    params = {
        "filters[title][$containsi]": "AUTOMATION"
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, article["documentId"])


def test_list_articles_filter_starts_with_slug(strapi_api, article_factory):
    article = article_factory(
        generate_article_payload(slug="automation_startslike_this")
    )
    params = {
        "filters[slug][$startsWith]": "automation_"
    }
    url = ArticleEndpoint.get_all(params)

    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_contains_document_id(response, article["documentId"])
    validate.data.item_field_equals(response, article["documentId"], "slug", article["slug"])


def test_list_articles_filter_ends_with_slug(strapi_api, article_factory):
    article = article_factory(
        generate_article_payload(slug="this_slug_must_end_correctly")
    )
    params = {
        "filters[slug][$endsWith]": "end_correctly"
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, article["documentId"])
    validate.data.item_field_equals(response, article["documentId"], "slug", article["slug"])


def test_list_articles_filter_published(strapi_api, module_article):
    params = {
        "filters[publishedAt][$notNull]": True
    }
    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_not_empty(response)
    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.item_field_not_null(response, module_article["documentId"], "publishedAt")

