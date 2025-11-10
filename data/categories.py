from faker import Faker

fake = Faker()


def generate_category_payload(name=None, slug=None, description=None, articles=None):
    final_name = name or fake.word().capitalize()
    final_slug = slug or final_name.lower().replace(" ", "-")

    payload = {
        "data": {
            "name": final_name,
            "slug": final_slug,
            "description": description or fake.sentence(nb_words=6)
        }
    }

    if articles is not None:
        payload["data"]["articles"] = {
            "connect": articles
        }

    return payload
