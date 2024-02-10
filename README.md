# django-pretty-response
This is a simple middleware in Django that creates clean-formatted responses, covering cases where Django and DRF are used to respond with API calls.
### 😄 Success
```json
{
  "ok": true,
  "result": { "your_defined_data": "value" }
}
```
### 😢 Failure
```json
{
  "ok": false
  "error": {
    "status_code": "HTTP Status Code",
    "code": "Defined Error Code (Only supported in DRF)",
    "message": "Detailed information about the error"
  }
}
```
## Usage
Add `django_pretty_response.middleware.ResponseMiddleware` to the end your MIDDLEWARE in settings.py.
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...
    "django_pretty_response.middleware.ResponseMiddleware" # Add this line!
]
```
## Examples
### Django Only
```python
from django.http import HttpResponse

def ping(request, *args, **kwargs):
  return HttpResponse("pong")
```
returns
```json
{
  "ok": true,
  "result": "pong"
}
```
---
```python
from django.http import HttpResponse

def ping(request, *args, **kwargs):
  return HttpResponse("not found", status=404)
```
returns
```json
{
  "ok": false
  "error": {
    "status_code": 404,
    "message": "not found"
  }
}
```
---
```python
from django.http import HttpResponseBadRequest

def ping(request, *args, **kwargs):
  return HttpResponseBadRequest("invalid parameter")
```
returns 
```json
{
  "ok": false
  "error": {
    "status_code": 400,
    "message": "invalid parameter"
  }
}
```

### DRF
```python
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def ping(request, *args, **kwargs):
    return Response("pong")
```
returns
```json
{
  "ok": true,
  "result": "pong"
}
```
---
```python
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

@api_view(['GET'])
def ping(request, *args, **kwargs):
    raise ValidationError(detail="check your parameters", code="invalid value")
```
returns
```json
{
  "ok": false
  "error": {
    "status_code": 400,
    "code": "invalid value",
    "message": "check your parameter"
  }
}
```
---
You can also customize your error fields.
```python
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def ping(request, *args, **kwargs):
    return Response({"hint": "check your parameters"}, status=400)
```
returns
```json
{
  "ok": false
  "error": {
    "status_code": 400,
    "hint": "check your parameters"
  }
}
```
