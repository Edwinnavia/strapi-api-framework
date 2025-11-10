from main.endpoints.category_endpoint import CategoryEndpoint


class CategoryHooks:

    @staticmethod
    def before_create(strapi_api, payload):
        url = CategoryEndpoint.create()
        return strapi_api.post(url, payload)

    @staticmethod
    def after_delete(strapi_api, document_id):
        url = CategoryEndpoint.delete(document_id)
        return strapi_api.delete(url)
