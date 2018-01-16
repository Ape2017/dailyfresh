from django.contrib import admin
from orders.models import OrderInfo,OrderGoods

# Register your models here.

admin.site.register(OrderInfo)
admin.site.register(OrderGoods)