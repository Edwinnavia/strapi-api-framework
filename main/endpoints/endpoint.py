from enum import Enum
from config.config import BASE_URI


class Endpoint(Enum):
    ARTICLE = f"{BASE_URI}/articles"
    AUTHOR = f"{BASE_URI}/authors"
    CATEGORY = f"{BASE_URI}/categories"
