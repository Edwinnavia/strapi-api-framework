from main.endpoints.endpoint import Endpoint
from main.endpoints.base_endpoint import BaseEndpoint


class CategoryEndpoint(BaseEndpoint):
    base_path = Endpoint.CATEGORY.value
