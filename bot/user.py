from utils import random_string
import random
import json


class User(object):
    created = False
    token = None

    def __init__(self):
        self.username = random_string(10)
        self.password = random_string(14)
        self.email = random_string(14) + "@domain.com"

    def signup_data(self):
        return json.dumps(
            {"email": self.email, "username": self.username, "password": self.password}
        )

    def creativity(self):
        return json.dumps({"title": random_string(15), "body": random_string(130)})

    def enjoy(self, max_num, content):
        num = random.randint(0, max_num)
        self.preferences = random.sample(content, num)
