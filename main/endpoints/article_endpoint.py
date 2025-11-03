from main.endpoints.endpoint import Endpoint
from main.endpoints.base_endpoint import BaseEndpoint


class ArticleEndpoint(BaseEndpoint):
    base_path = Endpoint.ARTICLE.value
