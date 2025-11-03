from core.request_manager import RequestManager
import json
from main.endpoints.article_endpoint import ArticleEndpoint


def test1():
    params = {
        "filters[title][$containsi]": "API",
        "pagination[pageSize]": 5,
        "sort": "createdAt:desc"
    }

    url = ArticleEndpoint.get_all(params=params)
    print(url)
