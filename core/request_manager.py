import requests


class RequestManager:
    @staticmethod
    def get(url, headers=None, params=None):
        return requests.get(url, headers=headers, params=params)

    @staticmethod
    def post(url, headers=None, json=None):
        return requests.post(url, headers=headers, json=json)

    @staticmethod
    def put(url, headers=None, json=None):
        return requests.put(url, headers=headers, json=json)

    @staticmethod
    def delete(url, headers=None):
        return requests.delete(url, headers=headers)
