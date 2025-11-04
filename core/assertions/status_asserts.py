from core.logger import setup_logger


class StatusValidator:
    def __init__(self, logger=None):
        self.logger = logger or setup_logger("status_validator")

    def _log(self, level: str, message: str):
        if self.logger:
            getattr(self.logger, level)(message)

    def _validate(self, response, expected_code: int):
        self._log("info", f"Validating status code {expected_code} for URL: {response.url}")

        actual_code = response.status_code
        assert actual_code == expected_code, (
            f"Expected status code {expected_code}, but got {actual_code}. "
            f"Response text: {response.text[:300]}"
        )

        self._log("info", f" Status code {expected_code} validated successfully for {response.url}")

        if expected_code == 200:
            assert response.text, "Expected non-empty response body, but got empty."
            self._log("debug", "Response body is not empty.")


    def ok(self, response):
        self._validate(response, 200)

    def no_content(self, response):
        self._validate(response, 204)

    def bad_request(self, response):
        self._validate(response, 400)

    def unauthorized(self, response):
        self._validate(response, 401)

    def forbidden(self, response):
        self._validate(response, 403)

    def not_found(self, response):
        self._validate(response, 404)

    def unprocessable_entity(self, response):
        self._validate(response, 422)

    def internal_server_error(self, response):
        self._validate(response, 500)
