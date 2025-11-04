from core.assertions.status_asserts import StatusValidator
from core.assertions.schema_asserts import SchemaValidator
from core.logger import setup_logger


class ValidationManager:
    def __init__(self):
        logger = setup_logger("validation_manager")
        self.status = StatusValidator(logger)
        self.schema = SchemaValidator(logger)
