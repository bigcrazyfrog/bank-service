from django.contrib import admin

from app.internal.admin.account_card import AccountAdmin, CardAdmin
from app.internal.admin.admin_user import AdminUserAdmin

admin.site.site_title = "Backend course"
admin.site.site_header = "Backend course"
