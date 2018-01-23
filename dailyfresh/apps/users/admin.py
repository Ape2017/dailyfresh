# django后台核心模块
from django.contrib import admin
# 用户模块
from users.models import User,Address


admin.site.register(User)
admin.site.register(Address)