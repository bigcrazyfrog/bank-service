from ninja import Router, NinjaAPI
from django.http import JsonResponse

from app.internal.bank.domain.entities import AccountListSchema, BalanceSchema, ErrorResponse, SuccessResponse
from app.internal.bank.presentation.handlers import AccountHandlers


def get_accounts_router(account_handlers: AccountHandlers):
    router = Router(tags=['account'])

    router.add_api_operation(
        '/get_list',
        ['GET'],
        account_handlers.get_list,
        response={200: AccountListSchema, 400: ErrorResponse},
    )

    router.add_api_operation(
        '/get_balance',
        ['GET'],
        account_handlers.get_balance,
        response={200: BalanceSchema, 400: ErrorResponse},
    )

    router.add_api_operation(
        '/exists',
        ['GET'],
        account_handlers.exists,
        response={200: SuccessResponse, 400: ErrorResponse},
    )

    router.add_api_operation(
        '/send_money',
        ['POST'],
        account_handlers.send_money,
        response={200: SuccessResponse, 400: ErrorResponse},
        auth=None,
    )

    router.add_api_operation(
        '/send_money_by_id',
        ['POST'],
        account_handlers.send_money_by_id,
        response={200: SuccessResponse, 400: ErrorResponse},
        auth=None,
    )

    return router


def add_accounts_router(api: NinjaAPI, account_handlers: AccountHandlers):
    account_handler = get_accounts_router(account_handlers)
    api.add_router('/account', account_handler)
