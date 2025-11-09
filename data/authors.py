from faker import Faker

fake = Faker()


def generate_author_payload(name=None, email=None, articles=None, avatar=None):
    payload = {
        "data": {
            "name": name or fake.first_name(),
            "email": email or fake.email(),
        }
    }

    if articles is not None:
        payload["data"]["articles"] = {
            "connect": articles
        }

    if avatar is not None:
        payload["data"]["avatar"] = avatar

    return payload
