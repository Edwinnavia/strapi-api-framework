from main.endpoints.article_endpoint import ArticleEndpoint


class ArticleHooks:

    @staticmethod
    def before_create(strapi_api, payload):
        url = ArticleEndpoint.create()
        return strapi_api.post(url, payload)

    @staticmethod
    def after_delete(strapi_api, document_id):
        url = ArticleEndpoint.delete(document_id)
        return strapi_api.delete(url)
