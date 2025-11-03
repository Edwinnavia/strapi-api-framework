from urllib.parse import urlencode
from main.endpoints.endpoint import Endpoint


class AuthorEndpoint:
    @classmethod
    def base(cls):
        return Endpoint.AUTHOR.value

    @classmethod
    def get_all(cls, params: dict = None):
        if params:
            query = urlencode(params, doseq=True)
            return f"{cls.base()}?{query}"
        return cls.base()

    @classmethod
    def get_by_id(cls, document_id: str):
        return f"{cls.base()}/{document_id}"

    @classmethod
    def create(cls):
        return cls.base()

    @classmethod
    def update(cls, document_id: str):
        return f"{cls.base()}/{document_id}"

    @classmethod
    def delete(cls, document_id: str):
        return f"{cls.base()}/{document_id}"
