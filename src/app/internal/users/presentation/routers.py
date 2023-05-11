from typing import List

from django.http import JsonResponse
from ninja import NinjaAPI, Router

from app.internal.users.domain.entities import ErrorResponse, SuccessResponse, Tokens, UserOut
from app.internal.users.presentation.handlers import IncorrectPasswordError, UserHandlers


def get_users_router(user_handlers: UserHandlers):
    router = Router(tags=['users'])

    router.add_api_operation(
        '',
        ['GET'],
        user_handlers.get_user_by_id,
        response={200: UserOut, 404: ErrorResponse},
    )

    router.add_api_operation(
        '/update_phone',
        ['PUT'],
        user_handlers.update_phone,
        response={200: SuccessResponse, 400: ErrorResponse}
    )

    router.add_api_operation(
        '/favorites',
        ['GET'],
        user_handlers.get_favorite_list,
        response={200: List[UserOut], 404: ErrorResponse},
    )

    router.add_api_operation(
        '/favorites/add',
        ['POST'],
        user_handlers.add_favorite,
        response={200: SuccessResponse, 400: ErrorResponse}
    )

    router.add_api_operation(
        '/favorites/remove',
        ['DELETE'],
        user_handlers.remove_favorite,
        response={200: SuccessResponse, 400: ErrorResponse}
    )

    return router


def add_users_router(api: NinjaAPI, user_handlers: UserHandlers):
    users_handler = get_users_router(user_handlers)
    api.add_router('/me', users_handler)
