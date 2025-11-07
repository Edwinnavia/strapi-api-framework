from core.logger import setup_logger
import pytest


class DataValidator:
    def __init__(self, logger=None):
        self.logger = logger or setup_logger("data_validator")

    def _log(self, level: str, message: str):
        if self.logger:
            getattr(self.logger, level)(message)

    def _extract_json(self, response):
        self._log("info", "Extracting JSON from response...")
        try:
            return response.json()
        except Exception as err:
            self._log("error", f"Failed to parse JSON: {err}")
            pytest.fail(f"Failed to decode response JSON: {err}", pytrace=False)

    def _ensure_data_field(self, response_json):
        if "data" not in response_json:
            self._log("error", "'data' field missing in response JSON")
            pytest.fail("Response JSON does not contain required field: 'data'", pytrace=False)

    def list_contains_document_id(self, response, document_id: str):
        response_json = self._extract_json(response)
        self._ensure_data_field(response_json)

        self._log("info", f"Checking if documentId '{document_id}' exists in the list...")

        items = response_json["data"]

        assert any(item.get("documentId") == document_id for item in items), (
            f"Expected documentId '{document_id}' not found in response list."
        )

        self._log("info", f"documentId '{document_id}' found successfully in response list.")

    def field_equals(self, response, field: str, expected_value):
        response_json = self._extract_json(response)

        self._log("info", f"Checking field '{field}' equals '{expected_value}'")

        actual_value = response_json.get(field)
        assert actual_value == expected_value, (
            f"Field '{field}' expected value '{expected_value}', but got '{actual_value}'"
        )

        self._log("info", f"Field '{field}' validated successfully.")

    def item_field_equals(self, response, document_id: str, field: str, expected_value):
        response_json = self._extract_json(response)
        self._ensure_data_field(response_json)

        self._log("info", f"Looking for item with documentId '{document_id}'...")

        items = response_json["data"]
        target = next((item for item in items if item.get("documentId") == document_id), None)

        assert target is not None, f"Item with documentId '{document_id}' not found."

        actual_value = target.get(field)
        assert actual_value == expected_value, (
            f"Expected '{field}' to be '{expected_value}', but got '{actual_value}'"
        )

        self._log("info", f"Field '{field}' validated for item {document_id}")

    def list_not_empty(self, response):
        response_json = self._extract_json(response)
        self._ensure_data_field(response_json)

        self._log("info", "Checking if response list is not empty...")

        assert len(response_json["data"]) > 0, "Expected list to be non-empty."

        self._log("info", "Response list is not empty.")
