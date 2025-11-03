import requests


class RequestManager:
    @staticmethod
    def get(url, headers=None, params=None):
        try:
            print(f"[GET] URL: {url}")
            response = requests.get(url, headers=headers, params=params)
            print(f"[GET] Status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] GET request failed: {e}")
            raise

    @staticmethod
    def post(url, headers=None, data=None, json=None):
        try:
            print(f"[POST] URL: {url}")
            response = requests.post(url, headers=headers, data=data, json=json)
            print(f"[POST] Status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] POST request failed: {e}")
            raise

    @staticmethod
    def put(url, headers=None, data=None, json=None):
        try:
            print(f"[PUT] URL: {url}")
            response = requests.put(url, headers=headers, data=data, json=json)
            print(f"[PUT] Status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] PUT request failed: {e}")
            raise

    @staticmethod
    def delete(url, headers=None, data=None, json=None):
        try:
            print(f"[DELETE] URL: {url}")
            response = requests.delete(url, headers=headers, data=data, json=json)
            print(f"[DELETE] Status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] DELETE request failed: {e}")
            raise
