from urllib.parse import urlencode


class BaseEndpoint:
    base_path = None

    @classmethod
    def base(cls):
        if not cls.base_path:
            raise NotImplementedError("The subclass must set 'base_path'.")
        return cls.base_path

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
