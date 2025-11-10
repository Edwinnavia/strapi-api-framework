from faker import Faker

fake = Faker()


def generate_category_payload(name=None, slug=None, description="__AUTO__", articles=None):
    final_name_original = name or fake.word().capitalize()
    final_name = str(final_name_original)
    final_slug = slug or final_name.lower().replace(" ", "-")

    payload = {
        "data": {
            "name": final_name_original,
            "slug": final_slug,
        }
    }

    if description == "__AUTO__":
        payload["data"]["description"] = fake.sentence(nb_words=6)
    else:
        payload["data"]["description"] = description

    if articles is not None:
        payload["data"]["articles"] = {
            "connect": articles
        }

    return payload
