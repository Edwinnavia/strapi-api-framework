from faker import Faker

fake = Faker()


def generate_article_payload(title=None, description=None, slug=None,
                             author=None, category=None):
    final_title_original = title or fake.sentence(nb_words=3).replace(".", "")
    final_title = str(final_title_original)
    payload = {
        "data": {
            "title": final_title_original,
            "description": description or fake.text(max_nb_chars=80),
            "slug": slug or final_title.lower().replace(" ", "-"),
        }
    }

    if author is not None:
        payload["data"]["author"] = author

    if category is not None:
        payload["data"]["category"] = category

    return payload
