from typing import List

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from telegram import Update
from telegram.ext import ContextTypes

import app.internal.responses.static_text as st
from app.internal.responses.services import log_errors, send_message
from app.internal.users.domain.entities import SuccessResponse, UserOut, UserSchema
from app.internal.users.domain.services import UserService


class UserHandlers:
    """User handler for API methods."""

    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def get_user_by_id(self, request: HttpRequest) -> UserOut:
        """Get current user."""
        user = self._user_service.get_user_by_id(id=request.user)
        return user

    def update_phone(self, request: HttpRequest, phone_number: str) -> SuccessResponse:
        """Provide set or update phone number."""
        self._user_service.update_phone(id=request.user, phone_number=phone_number)
        return SuccessResponse(success=True)

    def get_favorite_list(self, request: HttpRequest) -> List[UserOut]:
        """Show favourite list of user."""
        return self._user_service.get_favorite_list(id=request.user)

    def add_favorite(self, request: HttpRequest, favorite_user_id: str) -> SuccessResponse:
        """Add user to favourite list."""
        self._user_service.add_favorite(id=request.user, favorite_user_id=favorite_user_id)
        return SuccessResponse(success=True)

    def remove_favorite(self, request: HttpRequest, favorite_user_id: str) -> SuccessResponse:
        """Remove user from favourite list."""
        self._user_service.remove_favorite(id=request.user, favorite_user_id=favorite_user_id)
        return SuccessResponse(success=True)


class BotUserHandlers:
    """User handler for Telegram bot.

    Contain sync methods for interaction with user by Telegram bot API.

    """

    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @log_errors
    def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Register new user and send welcome message."""
        user = UserSchema(
            id=update.effective_chat.id,
            name=update.effective_chat.first_name,
        )

        self._user_service.add_user(user)
        send_message(update, context, st.welcome)

    @log_errors
    def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send help message."""
        send_message(update, context, st.help)

    @log_errors
    def set_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Provide set or change phone number."""
        text = st.success

        try:
            self._user_service.update_phone(update.effective_chat.id, context.args[0])
        except (IndexError, ValidationError):
            text = st.incorrect

        send_message(update, context, text)

    @log_errors
    def me(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get information about current user."""
        user = self._user_service.get_user_by_id(update.effective_chat.id)

        text = st.user_info(user)
        send_message(update, context, text)

    @log_errors
    def favorite_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show favourite list of user."""
        favorite_users = self._user_service.get_favorite_list(update.effective_chat.id)

        if favorite_users:
            text = st.favorite_list
            for user in favorite_users:
                text += '\n' + user.name
        else:
            text = st.favorite_no_list

        send_message(update, context, text)

    @log_errors
    def add_favorite(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Add user to favourite list.

        Note:
            Message should contain user ID.

        """
        text = st.user_not_found

        try:
            self._user_service.add_favorite(update.effective_chat.id, context.args[0])
            text = st.user_was_add
        except IndexError:
            text = st.incorrect_input

        send_message(update, context, text)

    @log_errors
    def remove_favorite(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Remove user from favourite list.

        Note:
            Message should contain user ID to remove.

        """
        text = st.user_not_found

        try:
            self._user_service.remove_favorite(update.effective_chat.id, context.args[0])
            text = st.user_was_remove
        except IndexError:
            text = st.incorrect_input

        send_message(update, context, text)

    @log_errors
    def set_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set new password for current user."""
        try:
            self._user_service.set_password(update.effective_chat.id, context.args[0])
            text = st.password_was_recorded
        except (IndexError, ValueError):
            text = st.incorrect_input

        send_message(update, context, text)
