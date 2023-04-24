from django.contrib import admin

from app.internal.admin.account_card import AccountAdmin, CardAdmin
from app.internal.admin.admin_user import AdminUserAdmin, UserAdmin
from app.internal.admin.transaction import TransactionAdmin

admin.site.site_title = "Backend course"
admin.site.site_header = "Backend course"
