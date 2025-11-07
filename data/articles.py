from faker import Faker

fake = Faker()


def generate_article_payload(title=None, description=None, slug=None,
                             author=None, category=None):
    payload = {
        "data": {
            "title": title or fake.sentence(nb_words=3).replace(".", ""),
            "description": description or fake.text(max_nb_chars=100),
            "slug": slug or fake.slug(),
        }
    }

    if author is not None:
        payload["data"]["author"] = author

    if category is not None:
        payload["data"]["category"] = category

    return payload
