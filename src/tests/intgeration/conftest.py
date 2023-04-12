import pytest
from unittest.mock import MagicMock

from telegram.ext import ApplicationBuilder


# @pytest.fixture(scope="function")
# def bot_app():
#     return ApplicationBuilder().build()

@pytest.fixture(scope="function")
def update():
    mock = MagicMock()
    mock.effective_chat.id = "1111111111"

    return mock

@pytest.fixture(scope="function")
def context():
    async def send_message(chat_id, text, parse_mode, reply_markup):
        assert text

    mock = MagicMock()
    mock.bot.send_message = send_message
    mock.bot.test_message = ''
    mock.args = []

    return mock
