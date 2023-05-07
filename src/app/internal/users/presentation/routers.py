from ninja import Router, NinjaAPI
from django.http import JsonResponse

from app.internal.users.domain.entities import SuccessResponse, ErrorResponse, UserOut, Tokens, \
    FavouriteListSchema
from app.internal.users.presentation.handlers import UserHandlers, IncorrectPasswordError


def get_users_router(user_handlers: UserHandlers):
    router = Router(tags=['users'])

    router.add_api_operation(
        '/login',
        ['GET'],
        user_handlers.login,
        response={200: Tokens, 400: ErrorResponse},
        auth=None,
    )

    router.add_api_operation(
        '/update_tokens',
        ['POST'],
        user_handlers.update_tokens,
        response={200: Tokens, 400: ErrorResponse},
        auth=None,
    )

    router.add_api_operation(
        '/add',
        ['POST'],
        user_handlers.add_user,
        response={200: SuccessResponse, 201: None, 400: ErrorResponse},
        auth=None,
    )

    router.add_api_operation(
        '/get_user/{user_id}',
        ['GET'],
        user_handlers.get_user_by_id,
        response={200: UserOut, 404: ErrorResponse},
        auth=None,
    )

    router.add_api_operation(
        '/get_favorite_list',
        ['GET'],
        user_handlers.get_favorite_list,
        response={200: FavouriteListSchema, 404: ErrorResponse},
    )

    router.add_api_operation(
        '/update_phone',
        ['PUT'],
        user_handlers.update_phone,
        response={200: SuccessResponse, 400: ErrorResponse}
    )

    router.add_api_operation(
        '/add_favorite',
        ['POST'],
        user_handlers.add_favorite,
        response={200: SuccessResponse, 400: ErrorResponse}
    )

    router.add_api_operation(
        '/remove_favorite',
        ['DELETE'],
        user_handlers.remove_favorite,
        response={200: SuccessResponse, 400: ErrorResponse}
    )

    return router


def add_users_router(api: NinjaAPI, user_handlers: UserHandlers):
    users_handler = get_users_router(user_handlers)
    api.add_router('/users', users_handler)
