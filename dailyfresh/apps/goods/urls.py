from django.conf.urls import url
from . import views

urlpatterns = [
    # 主页
    url(r"^$", views.IndexView.as_view(), name="index"),
    # sdu清单
    url(r"^list$", views.ListView.as_view(), name="list"),
    # 详情页
    url(r"^detail$", views.DetailView.as_view(), name="detail"),

]
