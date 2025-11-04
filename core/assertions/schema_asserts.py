import json
import pytest
from jsonschema import validate, exceptions as jsonschema_exceptions
from core.utils.resource_loader import load_schema_resource


class SchemaValidator:

    def __init__(self, logger=None):
        self.logger = logger

    def _log(self, level, message):
        if self.logger:
            getattr(self.logger, level)(message)

    def _load_and_validate_schema(self, data_json, category, schema_file):
        try:
            schema = load_schema_resource(category, schema_file)
            self._log("info", f"Loaded schema: {schema_file}")
        except FileNotFoundError:
            self._log("error", f"Schema file '{schema_file}' not found")
            pytest.fail(f"Schema file '{schema_file}' not found", pytrace=False)
        except json.JSONDecodeError as err:
            self._log("error", f"Failed to decode JSON schema: {err}")
            pytest.fail(f"Failed to decode JSON schema: {err}", pytrace=False)

        try:
            validate(instance=data_json, schema=schema)
            self._log("info", f"JSON schema validation passed: {schema_file}")
            return True
        except jsonschema_exceptions.ValidationError as err:
            self._log("error", f"Schema validation failed: {err.message}")
            pytest.fail(
                f"Schema validation failed: {err.message}\nPath: {list(err.path)}",
                pytrace=False,
            )
        except jsonschema_exceptions.SchemaError as err:
            self._log("error", f"Invalid JSON schema: {err.message}")
            pytest.fail(f"Invalid JSON schema: {err.message}", pytrace=False)

    def validate_response(self, response, category, schema_file):
        try:
            data_json = response.json()
            self._log("info", f"Validating response JSON against '{schema_file}'")
        except json.JSONDecodeError as err:
            self._log("error", f"Failed to decode response JSON: {err}")
            pytest.fail(f"Failed to decode response JSON: {err}", pytrace=False)
        return self._load_and_validate_schema(data_json, category, schema_file)

    def validate_payload(self, payload, category, schema_file):
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
                self._log("info", "Converted string payload to JSON object.")
            except json.JSONDecodeError as err:
                self._log("error", f"Failed to decode string payload JSON: {err}")
                pytest.fail(f"Failed to decode string payload JSON: {err}", pytrace=False)
        return self._load_and_validate_schema(payload, category, schema_file)
