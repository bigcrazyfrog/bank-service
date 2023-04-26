from http import HTTPStatus

from django.http import JsonResponse

incorrect_password = JsonResponse({"detail": "Incorrect password or username"}, status=HTTPStatus.UNAUTHORIZED)
invalid_token = JsonResponse({"detail": "Invalid token"}, status=HTTPStatus.UNAUTHORIZED)
