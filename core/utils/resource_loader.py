import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent


def resources_schemas_path(category: str, filename: str) -> Path:
    return BASE / "main" / "schemas" / category / filename


def load_schema_resource(category: str, filename: str) -> dict:
    schema_path = resources_schemas_path(category, filename)
    try:
        with schema_path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Schema '{filename}' not found in '{category}'")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in schema '{filename}': {e}")
