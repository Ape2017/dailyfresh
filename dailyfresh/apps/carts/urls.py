from django.conf.urls import url
from . import views

urlpatterns = [
    # 购物车增加
    url(r"^add$", views.AddView.as_view(), name="add"),
    # 购物车查询
    url(r"^info$", views.InfoView.as_view(), name="info"),
    # 购物车更新
    url(r"^update$", views.UpdateView.as_view(), name="update"),
    # 购物车删除
    url(r"^delete", views.DeleteView.as_view(), name="delete"),

]
