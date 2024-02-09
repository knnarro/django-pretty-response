import json

from django.http import HttpResponse


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        ok = 200 <= response.status_code < 400

        # for Django Only
        if isinstance(response, HttpResponse):
            response.headers["Content-Type"] = "application/json"
            content = {"ok": ok, "result": str(response.content, "utf-8")}

            if not ok:
                try:
                    has_content_html = content["result"].find("<!doctype html>") >= 0
                except Exception as e:
                    print(e)
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
