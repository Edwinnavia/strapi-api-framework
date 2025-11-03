from main.endpoints.endpoint import Endpoint
from main.endpoints.base_endpoint import BaseEndpoint


class AuthorEndpoint(BaseEndpoint):
    base_path = Endpoint.AUTHOR.value
