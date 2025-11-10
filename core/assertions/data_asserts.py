from core.logger import setup_logger
import pytest


class DataValidator:
    def __init__(self, logger=None):
        self.logger = logger or setup_logger("data_validator")

    def _log(self, level: str, message: str):
        getattr(self.logger, level)(message)

    def _extract_json(self, response):
        self._log("info", "Extracting JSON from response...")
        try:
            return response.json()
        except Exception as err:
            self._log("error", f"Failed to parse JSON: {err}")
            pytest.fail(f"Invalid JSON in response: {err}", pytrace=False)

    def _get_items(self, response):
        data = self._extract_json(response).get("data")
        if data is None:
            self._log("error", "'data' field missing in response.")
            pytest.fail("Response JSON missing required field: 'data'", pytrace=False)
        return data

    def _find_item(self, response, document_id: str):
        items = self._get_items(response)
        for item in items:
            if item.get("documentId") == document_id:
                return item

        pytest.fail(f"Item with documentId '{document_id}' not found.", pytrace=False)

    def list_contains_document_id(self, response, document_id: str):
        self._log("info", f"Checking if list contains documentId '{document_id}'...")
        items = self._get_items(response)

        if not any(item.get("documentId") == document_id for item in items):
            pytest.fail(f"DocumentId '{document_id}' not found in list.", pytrace=False)

        self._log("info", f"documentId '{document_id}' found successfully.")

    def list_not_empty(self, response):
        items = self._get_items(response)
        assert len(items) > 0, "Expected non-empty data array."
        self._log("info", "List is not empty.")

    def list_count_equals(self, response, expected_count: int):
        items = self._get_items(response)
        actual = len(items)
        assert actual == expected_count, f"Expected {expected_count} items, got {actual}"
        self._log("info", f"List has exactly {expected_count} items.")
        return True

    def list_not_contains_document_id(self, response, document_id: str):
        self._log("info", f"Validating documentId '{document_id}' is NOT present in list...")
        items = self._get_items(response)

        assert all(item.get("documentId") != document_id for item in items), (
            f"documentId '{document_id}' SHOULD NOT be present in response list, but it was found."
        )

        self._log("info", f"documentId '{document_id}' correctly NOT found in response list.")

    def item_field_equals(self, response, document_id: str, field: str, expected_value):
        self._log("info", f"Validating field '{field}' for documentId '{document_id}'...")
        item = self._find_item(response, document_id)

        actual_value = item.get(field)
        assert actual_value == expected_value, (
            f"Expected '{field}' = '{expected_value}', but got '{actual_value}'"
        )

        self._log("info", f"Field '{field}' validated successfully.")

    def response_field_equals(self, response, field: str, expected_value):
        self._log("info", f"Validating root-level field '{field}'...")
        payload = self._extract_json(response)

        actual_value = payload.get(field)
        assert actual_value == expected_value, (
            f"Expected response['{field}'] = '{expected_value}', got '{actual_value}'"
        )
        self._log("info", f"Root field '{field}' validated successfully.")

    def item_field_not_null(self, response, document_id: str, field: str):
        item = self._find_item(response, document_id)
        actual_value = item.get(field)
        assert actual_value is not None, (
            f"Expected '{field}' to be non-null for documentId '{document_id}', but got null"
        )

    def item_field_is_null(self, response, document_id, field):
        item = self._find_item(response, document_id)
        actual = item.get(field)
        assert actual is None, (
            f"Expected field '{field}' to be null, but got '{actual}'"
        )

    def nested_field_equals(self, response, document_id: str, parent_field: str, child_field: str, expected_value):
        item = self._find_item(response, document_id)

        nested_obj = item.get(parent_field)
        assert nested_obj is not None, (
            f"Parent field '{parent_field}' not found for documentId '{document_id}'."
        )

        actual_value = nested_obj.get(child_field)
        assert actual_value == expected_value, (
            f"Expected nested field '{parent_field}.{child_field}' "
            f"to be '{expected_value}', but got '{actual_value}'."
        )

        self._log(
            "info",
            f"Nested field '{parent_field}.{child_field}' validated successfully "
            f"for documentId '{document_id}'."
        )

    def pagination_exists(self, response):
        response_json = self._extract_json(response)

        self._log("info", "Checking pagination metadata existence...")

        pagination = response_json.get("meta", {}).get("pagination")
        assert pagination is not None, "Pagination metadata is missing."

        for field in ["page", "pageSize", "pageCount", "total"]:
            assert field in pagination, f"Pagination field '{field}' is missing."

        self._log("info", "Pagination metadata exists and contains required fields.")

    def pagination_value_equals(self, response, field: str, expected_value):
        self._log("info", f"Validating pagination field '{field}' equals '{expected_value}'...")
        pagination = self._extract_json(response).get("meta", {}).get("pagination", {})

        actual = pagination.get(field)
        assert actual == expected_value, (
            f"Expected pagination['{field}'] = {expected_value}, but got {actual}"
        )

        self._log("info", f"Pagination field '{field}' validated successfully.")

    def pagination_greater_equal(self, response, field: str, min_value: int):
        self._log("info", f"Validating pagination field '{field}' >= {min_value}...")
        pagination = self._extract_json(response).get("meta", {}).get("pagination", {})

        actual = pagination.get(field)
        assert actual >= min_value, (
            f"Expected pagination['{field}'] >= {min_value}, but got {actual}"
        )

        self._log("info", f"Pagination field '{field}' meets minimum requirement.")

    def pagination_matches(self, response, expected: dict):
        self._log("info", "Validating multiple pagination fields...")

        pagination = self._extract_json(response).get("meta", {}).get("pagination", {})

        for field, value in expected.items():
            actual = pagination.get(field)
            assert actual == value, (
                f"Expected pagination['{field}'] = {value}, but got {actual}"
            )

        self._log("info", "All pagination fields validated successfully.")

    def pagination_has_keys(self, response, keys: list[str]):
        body = self._extract_json(response)
        meta = body.get("meta", {})
        pagination = meta.get("pagination", {})
        for k in keys:
            assert k in pagination, f"Expected pagination key '{k}' not found"

    def pagination_missing_keys(self, response, keys: list[str]):
        body = self._extract_json(response)
        meta = body.get("meta", {})
        pagination = meta.get("pagination", {})
        for k in keys:
            assert k not in pagination, f"Pagination key '{k}' should NOT be present"

    def list_is_sorted_by(self, response, field: str, order: str = "asc"):
        items = self._get_items(response)
        values = [item.get(field) for item in items]
        sorted_values = sorted(values)
        if order.lower() == "desc":
            sorted_values = list(reversed(sorted_values))
        assert values == sorted_values, f"List not sorted by '{field}' {order}. Got {values}"

    def items_only_have_fields(self, response, allowed_fields: set[str]):
        items = self._get_items(response)
        for it in items:
            extra = set(it.keys()) - allowed_fields
            assert not extra, f"Unexpected fields present: {extra}"

    def items_all_have_fields(self, response, required_fields: set[str]):
        items = self._get_items(response)
        for it in items:
            missing = required_fields - set(it.keys())
            assert not missing, f"Missing required fields: {missing}"

    def nested_list_not_empty(self, response, document_id, parent_field):
        item = self._find_item(response, document_id)

        nested = item.get(parent_field)
        assert isinstance(nested, list), f"Expected '{parent_field}' to be a list"
        assert len(nested) > 0, f"Expected '{parent_field}' list to be non-empty"

    def item_field_greater_than(self, response, document_id: str, field: str, min_value):
        item = self._find_item(response, document_id)

        actual = item.get(field)
        assert actual is not None, f"Field '{field}' not found for documentId {document_id}"
        assert actual > min_value, (
            f"Expected '{field}' > {min_value}, but got {actual}"
        )

        self._log("info", f"Field '{field}' is greater than {min_value} as expected.")
