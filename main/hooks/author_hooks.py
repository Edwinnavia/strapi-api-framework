from main.endpoints.author_endpoint import AuthorEndpoint


class AuthorHooks:

    @staticmethod
    def before_create(strapi_api, payload):
        url = AuthorEndpoint.create()
        return strapi_api.post(url, payload)

    @staticmethod
    def after_delete(strapi_api, document_id):
        url = AuthorEndpoint.delete(document_id)
        return strapi_api.delete(url)
