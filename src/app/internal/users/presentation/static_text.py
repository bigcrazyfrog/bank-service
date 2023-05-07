from app.internal.users.domain.entities import UserOut

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

# phone number
success = "✅ Номер успешно записан"
incorrect = "❗ Введите корректный номер"
not_exist = "Вы еще не ввели номер :з"

info = "👤 <b>Личный кабинет</b>"
line = "\n--------------------\n"

password_was_recorded = "✅ Пароль успешно записан"

# favorite users list
user_not_found = "Пользователь не найден"
user_was_remove = "Пользователь удален из избранного"
user_was_add = "Пользователь добавлен в избранное"
favorite_list = "⭐ <b>Избранный список</b>\n\n"
favorite_no_list = "Еще нет пользователей в избранном"


def me(user: UserOut) -> str:
    number = user.phone_number

    if number is None:
        return not_exist

    text = info + line
    text += f'🆔 Telegram ID : {user.id}\n ' \
            f'📞 Ваш номер : {number}' + line

    return text
