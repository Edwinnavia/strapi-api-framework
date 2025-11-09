from main.endpoints.article_endpoint import ArticleEndpoint
from main.validation_manager import ValidationManager

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
    validate.data.item_field_equals(response, module_article["documentId"], "documentId", module_article["documentId"])
    validate.data.item_field_equals(response, module_article["documentId"], "title", module_article["title"])
    validate.data.item_field_equals(response, module_article["documentId"], "slug", module_article["slug"])


def test_list_articles_filter_by_exact_title_case_insensitive(strapi_api, module_article):
    original_title = module_article["title"]
    mixed_case_title = original_title.swapcase()
    params = {
        "filters[title][$eqi]": mixed_case_title
    }

    url = ArticleEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "article", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.item_field_equals(response, module_article["documentId"], "title", module_article["title"])
    validate.data.item_field_equals(response, module_article["documentId"], "slug", module_article["slug"])


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
    published_at = module_article["publishedAt"]
    params = {
        "filters[publishedAt][$ne]": published_at
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

    validate.data.list_count_equals(response, 2)

    validate.data.list_contains_document_id(response, module_article["documentId"])
    validate.data.item_field_equals(response, module_article["documentId"], "title", module_article["title"])

    validate.data.list_contains_document_id(response, second_article["documentId"])
    validate.data.item_field_equals(response, second_article["documentId"], "slug", second_article["slug"])


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
    validate.data.item_field_equals(response, module_article["documentId"], "title", module_article["title"])
    validate.data.item_field_equals(response, module_article["documentId"], "slug", module_article["slug"])
