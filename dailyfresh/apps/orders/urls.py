from django.conf.urls import url
from . import views

urlpatterns = [

    url(r"^porder$", views.POrderView.as_view(), name="porder"),
    # 全部用户订单
    url(r'^order$', views.OrderView.as_view(), name="order"),

]
