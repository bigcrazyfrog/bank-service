from app.internal.users.domain.entities import UserOut

# general
welcome = "✅ <b>Добро пожаловать</b>! ✅\n\n" \
          "Список доступных команд - /help"
help = "🗓️ <b>Основные команды</b>\n\n" \
       "/start - запуск бота\n" \
       "/me - личный кабинет\n" \
       "/set_phone &lt;номер&gt; - записать телефон\n\n" \
       "/favorite_list - список избранных пользователей\n" \
       "/add_favorite &lt;id_пользователя&gt; - добавить в избранное\n" \
       "/remove_favorite &lt;id_пользователя&gt; - удалить из избранного\n\n" \
       "/account_list - список счетов в банке\n" \
       "/card_list - список карт\n" \
       "/balance &lt;номер_счета&gt; - баланс счета\n" \
       "/send_money - отправить деньги\n" \
       "/history &lt;номер_счета&gt; - история операций\n" \
       "/interaction - пользователи, с которыми было взаимодействие"

# Phone number
success = "✅ Номер успешно записан"
incorrect = "❗ Введите корректный номер"
not_exist = "Вы еще не ввели номер :з"

info = "👤 <b>Личный кабинет</b>"
line = "\n--------------------\n"

password_was_recorded = "✅ Пароль успешно записан"

# Favorite users list
user_not_found = "Пользователь не найден"
user_was_remove = "Пользователь удален из избранного"
user_was_add = "Пользователь добавлен в избранное"
favorite_list = "⭐ <b>Избранный список</b>\n\n"
favorite_no_list = "Еще нет пользователей в избранном"

# Account
account_was_created = "✅ Счет успешно создан\n\n"
account_is_exist = "⚠️ У вас уже есть счет\n\n" \
                   "/account_list - список счетов"

# Card
balance = "💸 Ваш баланс: "
balance_not_exist = "У вас нет счетов в банке.\n\n" \
                    "/create_account - создать пробный счет"
account_not_find = "Счет не найден."
account_list = "Ваши счета: \n\n"
card_list = "Ваши карты: \n\n"

# Transactions
no_access = "У вас неподтвержденный акквунт, для подтверждения обратитесь в поддержку"
choose_card = "📋 Выберите карту из выпадающего списка или введите вручную\n\n" \
              "/cancel - отмена операции"
not_found = "❗ Неверный номер, либо карты не существует\n\n" \
            "<i>*попробуйте снова</i>"
enter_amount = "💰 Введите сумму:"
incorrect_input = "❗ Введите корректное значение"
no_money = "Недостаточно средств на карте :3"
transaction_type = "Выберите тип перевода"
send_to_telegram_id = "Введите Telegram ID для перевода:"
send_to_bank_account = "Введите номер счета для перевода:"
send_to_card_number = "Введите номер карты для перевода:"
pitiful_attempt = "Пытаетесь отправить деньги самому себе??) 🤡"
not_in_favorite = "У этого пользователя неподтвержденный аккаунт"
successful = "✅ Перевод выполнен <b>успешно</b>! ✅"
user_not_fount = "❗ Неверный id, либо пользователя не существует\n\n" \
                 "<i>*попробуйте снова</i>"
incorrect_account = "Неверный номер, либо счета не существует"
error = "Что-то пошло не так... перевод не выполнен, обратитесь в поддержку"
cancelled = "❌️ Операция отменена"

send_postcard = "Выберите открытку"

# History
account_history = "📝 <b>История операций</b> 📝\n\n"
interaction_list = "👥 <b>Недавние пользователи</b> \n\n"
interaction_not_found = "Еще не было взаимодействий"


def user_info(user: UserOut) -> str:
    """Get information about user."""
    number = user.phone_number

    if number is None:
        return not_exist

    text = info + line
    text += f'🆔 Telegram ID : {user.id}\n ' \
            f'📞 Ваш номер : {number}' + line

    return text


def transaction_history(history, account: str) -> str:
    """Getting string with transaction history.

    Raises:
        ValueError: Raise if history is empty.

    """
    if len(history) == 0:
        raise ValueError

    text = account_history
    last_date = None
    for transaction in history:
        date = transaction.date.strftime('%b %d')
        if last_date != date:
            last_date = date
            text += f'[ {last_date} ]\n'

        amount = transaction.amount
        if amount == int(amount):
            amount = int(amount)

        if str(transaction.to_account.number) == account:
            text += f"➡️ <b>Входящий перевод</b> + {amount}₽\n" \
                    f"      От - {transaction.to_account.owner.name}, "
        else:
            text += f"💳 <b>Исходящий перевод</b> {amount}₽\n" \
                    f"      Кому - {transaction.to_account.owner.name}, "

        if transaction.postcard is not None:
            text += f"  <a href='{transaction.postcard}'>Открытка</a>\n"
        text += f'      Время - {transaction.date.strftime("%H:%M")}\n\n'

    return text
