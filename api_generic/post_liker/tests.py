from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
import json


class AnimalTestCase(TestCase):
    # python manage.py dumpdata --exclude auth.permission --exclude contenttypes --natural-foreign > post_liker/fixtures/test_data.json
    # python manage.py test post_liker
    fixtures = ["test_data.json"]

    def testLogin(self):
        c = Client()
        resp = c.post(
            reverse("liker:token_obtain_pair"),
            HTTP_AUTHORIZATION="Basic YWRtaW46YWRtaW4xOTkw",
        )
        js = json.loads(resp.content)
        self.assertTrue("access" in js)
        self.assertTrue("refresh" in js)

    def testLkersAnalysis(self):
        c = Client()
        resp = c.post(
            reverse("liker:token_obtain_pair"),
            HTTP_AUTHORIZATION="Basic YWRtaW46YWRtaW4xOTkw",
        )
        js = json.loads(resp.content)
        new_auth = f"Bearer {js['access']}"
        results = c.get(
            reverse("liker:likes_analysis"),
            {"date_from": "2020-04-21", "date_to": "2020-04-23"},
            HTTP_AUTHORIZATION=new_auth,
        )
        with open(
            "post_liker/fixtures/expected_results/analytics_sample1.json", "r"
        ) as f:
            exp_res = json.loads(f.read())
            self.assertEqual(exp_res, json.loads(results.content))
