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
