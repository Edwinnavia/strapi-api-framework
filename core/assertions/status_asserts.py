from core.logger import setup_logger

logger = setup_logger('status_validator')


class StatusValidator:

    @staticmethod
    def validate(response, expected_code: int):
        logger.info(f"Validating status code {expected_code} for URL: {response.url}")
        actual_code = response.status_code

        assert actual_code == expected_code, (
            f"Expected status code {expected_code}, but got {actual_code}. "
            f"Response text: {response.text[:300]}"
        )
        logger.info(f"Status code {expected_code} validated successfully for {response.url}")

        if expected_code == 200:
            assert response.text, "Expected non-empty response body, but got empty."
            logger.debug("Response body is not empty.")

    @staticmethod
    def ok(response):
        StatusValidator.validate(response, 200)

    @staticmethod
    def no_content(response):
        StatusValidator.validate(response, 204)

    @staticmethod
    def bad_request(response):
        StatusValidator.validate(response, 400)

    @staticmethod
    def unauthorized(response):
        StatusValidator.validate(response, 401)

    @staticmethod
    def forbidden(response):
        StatusValidator.validate(response, 403)

    @staticmethod
    def not_found(response):
        StatusValidator.validate(response, 404)

    @staticmethod
    def unprocessable_entity(response):
        StatusValidator.validate(response, 422)

    @staticmethod
    def internal_server_error(response):
        StatusValidator.validate(response, 500)
