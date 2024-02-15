import json

from django.test import TestCase


class ResponseTestCase(TestCase):
    def test_get_response_success(self):
        response = self.client.get("/success")
        response_body = json.loads(response.content)
        expected_body = {"ok": True, "result": "success"}
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response_body, expected_body)

    def test_get_response_bad_request(self):
        response = self.client.get("/bad-request")
        response_body = json.loads(response.content)
        expected_body = {
            "ok": False,
            "error": {"status_code": 400, "message": "invalid parameter"},
        }
        self.assertEqual(response.status_code, expected_body["error"]["status_code"])
        self.assertDictEqual(response_body, expected_body)

    def test_get_response_status_400(self):
        response = self.client.get("/status-400")
        response_body = json.loads(response.content)
        expected_body = {
            "ok": False,
            "error": {"status_code": 400, "message": "invalid parameter"},
        }
        self.assertEqual(response.status_code, expected_body["error"]["status_code"])
        self.assertDictEqual(response_body, expected_body)

    def test_get_drf_response_success(self):
        response = self.client.get("/drf/success")
        response_body = json.loads(response.content)
        expected_body = {"ok": True, "result": "success"}
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response_body, expected_body)

    def test_get_drf_response_status_400(self):
        response = self.client.get("/drf/bad-request")
        response_body = json.loads(response.content)
        expected_body = {
            "ok": False,
            "error": {"status_code": 400, "message": "invalid parameter"},
        }
        self.assertEqual(response.status_code, expected_body["error"]["status_code"])
        self.assertDictEqual(response_body, expected_body)

    def test_get_drf_response_status_400_custom(self):
        response = self.client.get("/drf/bad-request-custom")
        response_body = json.loads(response.content)
        expected_body = {
            "ok": False,
            "error": {"status_code": 400, "hint": "check request parameters"},
        }
        self.assertEqual(response.status_code, expected_body["error"]["status_code"])
        self.assertDictEqual(response_body, expected_body)

    def test_get_drf_response_status_400_custom_list(self):
        response = self.client.get("/drf/bad-request-custom-list")
        response_body = json.loads(response.content)
        expected_body = {
            "ok": False,
            "error": {"status_code": 400, "message": ["check request parameters"]},
        }
        self.assertEqual(response.status_code, expected_body["error"]["status_code"])
        self.assertDictEqual(response_body, expected_body)

    def test_raise_drf_validation_error(self):
        response = self.client.get("/drf/error")
        response_body = json.loads(response.content)
        expected_body = {
            "ok": False,
            "error": {
                "status_code": 400,
                "code": "invalid parameter",
                "message": "check request parameters",
            },
        }
        self.assertEqual(response.status_code, expected_body["error"]["status_code"])
        self.assertDictEqual(response_body, expected_body)

    def test_request_not_exist_url(self):
        response = self.client.get("/not-exist")
        response_body = json.loads(response.content)
        expected_body = {
            "ok": False,
            "error": {"status_code": 404, "message": "Not Found"},
        }
        self.assertEqual(response.status_code, expected_body["error"]["status_code"])
        self.assertDictEqual(response_body, expected_body)
