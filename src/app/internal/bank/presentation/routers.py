from django.http import JsonResponse
from ninja import NinjaAPI, Router

from app.internal.bank.domain.entities import AccountListSchema, BalanceSchema, CardListSchema
from app.internal.bank.presentation.handlers import BankHandlers
from app.internal.users.domain.entities import ErrorResponse, SuccessResponse


def get_banks_router(account_handlers: BankHandlers):
    router = Router(tags=['bank'])

    router.add_api_operation(
        '/accounts',
        ['GET'],
        account_handlers.get_account_list,
        response={200: AccountListSchema, 400: ErrorResponse},
    )

    router.add_api_operation(
        '/cards',
        ['GET'],
        account_handlers.get_card_list,
        response={200: CardListSchema, 400: ErrorResponse},
    )

    router.add_api_operation(
        '/balance',
        ['GET'],
        account_handlers.get_balance,
        response={200: BalanceSchema, 400: ErrorResponse},
    )

    router.add_api_operation(
        '/send_money',
        ['POST'],
        account_handlers.send_money,
        response={200: SuccessResponse, 400: ErrorResponse},
    )

    router.add_api_operation(
        '/send_money/by_id',
        ['POST'],
        account_handlers.send_money_by_id,
        response={200: SuccessResponse, 400: ErrorResponse},
    )

    return router


def add_banks_router(api: NinjaAPI, bank_handlers: BankHandlers):
    bank_handler = get_banks_router(bank_handlers)
    api.add_router('/bank', bank_handler)
