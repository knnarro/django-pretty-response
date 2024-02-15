from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError


def get_response_success(request):
    return HttpResponse("success")


def get_response_bad_request(request):
    return HttpResponseBadRequest("invalid parameter")


def get_response_status_400(request):
    return HttpResponse("invalid parameter", status=400)


@api_view(["GET"])
def get_drf_response_success(request):
    return Response("success")


@api_view(["GET"])
def get_drf_response_status_400(request):
    return Response("invalid parameter", status=400)


@api_view(["GET"])
def get_drf_response_status_400_custom(request):
    return Response({"hint": "check request parameters"}, status=400)


@api_view(["GET"])
def get_drf_response_status_400_custom_list(request):
    return Response(["check request parameters"], status=400)


@api_view(["GET"])
def raise_drf_validation_error(request):
    raise ValidationError(detail="check request parameters", code="invalid parameter")


urlpatterns = [
    path("success", get_response_success),
    path("bad-request", get_response_bad_request),
    path("status-400", get_response_status_400),
    path("drf/success", get_drf_response_success),
    path("drf/bad-request", get_drf_response_status_400),
    path("drf/bad-request-custom", get_drf_response_status_400_custom),
    path("drf/bad-request-custom-list", get_drf_response_status_400_custom_list),
    path("drf/error", raise_drf_validation_error),
]
