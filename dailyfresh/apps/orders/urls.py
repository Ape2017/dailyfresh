from django.conf.urls import url
from . import views

urlpatterns = [

    url(r"^palce$", views.PlaceOrderView.as_view(), name="place"),
    # 全部用户订单
    url(r'^commit$', views.CommitOrderView.as_view(), name="commit"),

]
