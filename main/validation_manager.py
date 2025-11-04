from core.assertions.status_asserts import StatusValidator


class ValidationManager:
    def __init__(self):
        self.status = StatusValidator()
