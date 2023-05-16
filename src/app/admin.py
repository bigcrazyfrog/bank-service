from django.contrib import admin

from app.internal.bank.presentation.admin import AccountAdmin, CardAdmin, TransactionAdmin
from app.internal.users.presentation.admin import UserAdmin

admin.site.site_title = "Backend course"
admin.site.site_header = "Backend course"
