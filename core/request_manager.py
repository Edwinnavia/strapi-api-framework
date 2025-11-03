import requests
from core.logger import setup_logger

logger = setup_logger("request_manager")


class RequestManager:
    @staticmethod
    def get(url, headers=None, params=None):
        try:
            logger.info(f"GET Request → URL: {url} | Headers: {headers} | Params: {params}")
            response = requests.get(url, headers=headers, params=params)
            logger.info(f"Response [GET] Status: {response.status_code} | Body: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"GET Request failed → {e}")
            raise

    @staticmethod
    def post(url, headers=None, data=None, json=None):
        try:
            logger.info(f"POST Request → URL: {url} | Headers: {headers}")
            logger.debug(f"Body: {json or data}")
            response = requests.post(url, headers=headers, data=data, json=json)
            logger.info(f"Response [POST] Status: {response.status_code} | Body: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"POST Request failed → {e}")
            raise

    @staticmethod
    def put(url, headers=None, data=None, json=None):
        try:
            logger.info(f"PUT Request → URL: {url} | Headers: {headers}")
            logger.debug(f"Body: {json or data}")
            response = requests.put(url, headers=headers, data=data, json=json)
            logger.info(f"Response [PUT] Status: {response.status_code} | Body: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"PUT Request failed → {e}")
            raise

    @staticmethod
    def delete(url, headers=None, data=None, json=None):
        try:
            logger.info(f"DELETE Request → URL: {url} | Headers: {headers}")
            response = requests.delete(url, headers=headers, data=data, json=json)
            logger.info(f"Response [DELETE] Status: {response.status_code} | Body: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"DELETE Request failed → {e}")
            raise
