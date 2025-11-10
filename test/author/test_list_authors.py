import pytest
from main.endpoints.author_endpoint import AuthorEndpoint
from main.validation_manager import ValidationManager
from data.authors import generate_author_payload

validate = ValidationManager()
pytestmark = pytest.mark.list_authors


# ============================================================
# TC-AU-01 - Consultar autores sin filtros aplicados
# ============================================================
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_without_filters(strapi_api, module_author):
    url = AuthorEndpoint.get_all()
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_contains_document_id(response, module_author["documentId"])
    validate.data.item_field_equals(response, module_author["documentId"], "name", module_author["name"])
    validate.data.item_field_equals(response, module_author["documentId"], "email", module_author["email"])


# ============================================================
# TC-AU-02 - Paginación por defecto
# ============================================================
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_default_pagination(strapi_api):
    url = AuthorEndpoint.get_all()
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.pagination_value_equals(response, "page", 1)
    validate.data.pagination_value_equals(response, "pageSize", 25)


# ============================================================
# TC-AU-03 - Paginación personalizada
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_custom_pagination(strapi_api):
    params = {"pagination[page]": 2, "pagination[pageSize]": 5}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.pagination_value_equals(response, "page", 2)
    validate.data.pagination_value_equals(response, "pageSize", 5)


# ============================================================
# TC-AU-04 - List authors with populated articles
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_with_populate_articles(strapi_api, module_author):
    params = {"populate": "articles"}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_contains_document_id(response, module_author["documentId"])
    validate.data.nested_list_not_empty(response, document_id=module_author["documentId"],
                                        parent_field="articles")


# ============================================================
# TC-AU-05 - Selección de campos específicos
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_select_specific_fields(strapi_api):
    params = {"fields[0]": "name", "fields[1]": "email"}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.items_only_have_fields(response, allowed_fields={"id", "documentId", "name", "email"})
    validate.data.items_all_have_fields(response, required_fields={"name", "email"})


# ============================================================
# TC-AU-06 - Sort authors by name ascending
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_sorted_by_name_asc(strapi_api):
    params = {"sort": "name:asc"}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_is_sorted_by(response, field="name", order="asc")


# ============================================================
# TC-AU-07 - Orden por fecha de creación desc
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_sorted_by_created_desc(strapi_api):
    params = {"sort": "createdAt:desc"}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_is_sorted_by(response, field="createdAt", order="desc")


# ============================================================
# TC-AU-08 - Filter authors by exact name ($eq)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_filter_exact_name(strapi_api, module_author):
    params = {"filters[name][$eq]": module_author["name"]}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_author["documentId"])
    validate.data.item_field_equals(response, module_author["documentId"], "name", module_author["name"])


# ============================================================
# TC-AU-09 - Exact name match (case-insensitive) ($eqi)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_filter_exact_name_case_insensitive(strapi_api, module_author):
    params = {"filters[name][$eqi]": module_author["name"].swapcase()}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_author["documentId"])
    validate.data.item_field_equals(response, module_author["documentId"], "name", module_author["name"])


# ============================================================
# TC-AU-10 - Email contains ($contains)
# ============================================================
@pytest.mark.authors
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_filter_email_contains(strapi_api, module_author):
    email_fragment = module_author["email"].split("@")[0]
    params = {"filters[email][$contains]": email_fragment}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_not_empty(response)
    validate.data.list_contains_document_id(response, module_author["documentId"])
    validate.data.item_field_equals(response, module_author["documentId"], "email", module_author["email"])


# ============================================================
# TC-AU-11 - Combined filters: name AND email
# ============================================================
@pytest.mark.authors
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_filter_name_and_email(strapi_api, module_author):
    params = {
        "filters[name][$eq]": module_author["name"],
        "filters[email][$eq]": module_author["email"],
    }
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_author["documentId"])
    validate.data.item_field_equals(response, module_author["documentId"], "name", module_author["name"])
    validate.data.item_field_equals(response, module_author["documentId"], "email", module_author["email"])


# ============================================================
# TC-AU-12 - Logical OR: name OR email
# ============================================================
@pytest.mark.authors
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_filter_or(strapi_api, module_author, author_factory):
    second_author = author_factory()
    params = {
        "filters[$or][0][name][$eq]": module_author["name"],
        "filters[$or][1][email][$eq]": second_author["email"],
    }
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_contains_document_id(response, module_author["documentId"])
    validate.data.list_contains_document_id(response, second_author["documentId"])


# ============================================================
# TC-AU-13 - Logical AND: name AND email
# ============================================================
@pytest.mark.authors
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_filter_and(strapi_api, module_author):
    params = {
        "filters[$and][0][name][$eq]": module_author["name"],
        "filters[$and][1][email][$eq]": module_author["email"],
    }
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_count_equals(response, 1)
    validate.data.list_contains_document_id(response, module_author["documentId"])


# ============================================================
# TC-AU-14 - withCount=false (should not return total/pageCount)
# ============================================================
@pytest.mark.authors
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_without_count(strapi_api):
    params = {"pagination[withCount]": "false"}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.pagination_has_keys(response, ["page", "pageSize"])
    validate.data.pagination_missing_keys(response, ["total", "pageCount"])


# ============================================================
# TC-AU-15 - populate + fields
# ============================================================
@pytest.mark.authors
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_populate_and_fields(strapi_api):
    params = {
        "populate": "articles",
        "fields[0]": "name",
        "fields[1]": "email"
    }
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_not_empty(response)
    allowed = {"name", "email", "id", "documentId", "articles"}
    validate.data.items_only_have_fields(response, allowed_fields=allowed)
    required = {"name", "email"}
    validate.data.items_all_have_fields(response, required_fields=required)


# ============================================================
# TC-AU-16 - Filter by name AND sort by createdAt ASC
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_filter_and_sort(strapi_api, module_author):
    params = {
        "filters[name][$eq]": module_author["name"],
        "sort": "createdAt:asc"
    }
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_contains_document_id(response, module_author["documentId"])
    validate.data.list_is_sorted_by(response, field="createdAt", order="asc")


# ============================================================
# TC-AU-17 - Filter by ID greater than ($gt)
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_filter_id_gt(strapi_api, module_author):
    params = {"filters[id][$gt]": module_author["id"] - 1}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.list_contains_document_id(response, module_author["documentId"])

    validate.data.item_field_greater_than(response, module_author["documentId"], field="id",
                                          min_value=module_author["id"] - 1)


# ============================================================
# TC-AU-18 - Combined pagination + filters + sorting
# ============================================================
@pytest.mark.positive
@pytest.mark.functional
def test_list_authors_combined_params(strapi_api):
    params = {
        "pagination[pageSize]": 10,
        "filters[name][$contains]": "a",
        "sort": "createdAt:desc",
    }
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)
    validate.schema.validate_response(response, "author", "list_response_schema.json")
    validate.data.pagination_exists(response)
    validate.data.pagination_value_equals(response, "pageSize", 10)
    validate.data.list_not_empty(response)
    validate.data.list_is_sorted_by(response, field="createdAt", order="desc")
    validate.data.items_field_contains(response, field="name", substring="a")


# ============================================================
# TC-AU-19 - pagination[page] as string (BUG)
# ID: TC-AU-19 | Name: Invalid page type (string)
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi returns 500 when pagination[page] is a string", strict=False)
def test_list_authors_page_string(strapi_api):
    params = {"pagination[page]": "asdasd"}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)


# ============================================================
# TC-AU-20 - pagination[pageSize] negative value (BUG)
# ID: TC-AU-20 | Name: Invalid negative pageSize
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi does not validate negative pageSize", strict=False)
def test_list_authors_page_size_negative(strapi_api):
    params = {"pagination[pageSize]": -1}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)


# ============================================================
# TC-AU-21 - pagination[pageSize] string (BUG)
# ID: TC-AU-21 | Name: Invalid pageSize type (string)
# ============================================================
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: Strapi returns 500 when pageSize is text", strict=False)
def test_list_authors_page_size_string(strapi_api):
    params = {"pagination[pageSize]": "uno"}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)


# ============================================================
# TC-AU-22 - malformed filter key ignored
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_list_authors_malformed_filter(strapi_api):
    params = {"filters[name][$eq": "test"}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.ok(response)


# ============================================================
# TC-AU-23 - invalid filter field ignored
# ============================================================
@pytest.mark.negative
@pytest.mark.functional
def test_list_authors_invalid_filter_field(strapi_api):
    params = {"filters[abc]": "123"}
    url = AuthorEndpoint.get_all(params)
    response = strapi_api.get(url)

    validate.status.bad_request(response)


