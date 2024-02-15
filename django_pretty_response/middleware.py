import json

from django.http import HttpResponse as DjangoResponse
from rest_framework.response import Response as DrfResponse
from rest_framework.exceptions import ErrorDetail


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        ok = 200 <= response.status_code < 400

        # for DRF
        if isinstance(response, DrfResponse):
            data = {"ok": ok, "result": response.data}

            if not ok:
                if isinstance(data["result"], dict):
                    error = {"status_code": response.status_code, **data["result"]}
                elif isinstance(data["result"], list) and isinstance(
                    data["result"][0], ErrorDetail
                ):
                    error = {
                        "status_code": response.status_code,
                        "message": data["result"][0],
                        "code": data["result"][0].code,
                    }
                else:
                    error = {
                        "status_code": response.status_code,
                        "message": data["result"],
                    }
                data["error"] = error
                data.pop("result")

            response.data = data
            response._is_rendered = False
            response.render()
            return response

        # for Django Only
        if isinstance(response, DjangoResponse):
            response.headers["Content-Type"] = "application/json"
            content = {"ok": ok, "result": str(response.content, "utf-8")}

            if not ok:
                has_content_html = content["result"].find("</html>") >= 0
                error = {
                    "status_code": response.status_code,
                    "message": content["result"]
                    if not has_content_html
                    else response.reason_phrase,
                }
                content["error"] = error
                content.pop("result")

            response.content = json.dumps(content)
            return response

        return response
