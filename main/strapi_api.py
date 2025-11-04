from config.config import API_TOKEN
from core.request_manager import RequestManager
from core.logger import setup_logger

logger = setup_logger("strapi_api")


class StrapiApi:
    def __init__(self):
        self.api_token = API_TOKEN

    def build_headers(self, custom_headers: dict | None = None, with_auth: bool = True) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if with_auth and self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        if custom_headers:
            headers.update(custom_headers)

        return headers

    def get(self, url: str, params: dict | None = None, headers: dict | None = None, with_auth: bool = True):
        final_headers = self.build_headers(headers, with_auth)
        logger.info(f"[GET] {url} | Params: {params} | Headers: {final_headers}")
        response = RequestManager.get(url, headers=final_headers, params=params)
        logger.info(f"→ Response [GET {response.status_code}]: {response.text[:200]}...")
        return response

    def post(self, url: str, payload: dict | None = None, headers: dict | None = None, with_auth: bool = True):
        final_headers = self.build_headers(headers, with_auth)
        logger.info(f"[POST] {url} | Payload: {payload} | Headers: {final_headers}")
        response = RequestManager.post(url, headers=final_headers, json=payload)
        logger.info(f"→ Response [POST {response.status_code}]: {response.text[:200]}...")
        return response

    def put(self, url: str, payload: dict | None = None, headers: dict | None = None, with_auth: bool = True):
        final_headers = self.build_headers(headers, with_auth)
        logger.info(f"[PUT] {url} | Payload: {payload} | Headers: {final_headers}")
        response = RequestManager.put(url, headers=final_headers, json=payload)
        logger.info(f"→ Response [PUT {response.status_code}]: {response.text[:200]}...")
        return response

    def delete(self, url: str, headers: dict | None = None, with_auth: bool = True):
        final_headers = self.build_headers(headers, with_auth)
        logger.info(f"[DELETE] {url} | Headers: {final_headers}")
        response = RequestManager.delete(url, headers=final_headers)
        if response.status_code == 204:
            logger.info(f"→ Response [DELETE {response.status_code}]: No Content (eliminación exitosa)")
        else:
            body_preview = response.text[:200] if response.text else "<sin cuerpo>"
            logger.info(f"→ Response [DELETE {response.status_code}]: {body_preview}")

        return response
