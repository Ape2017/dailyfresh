# django核心模块中的url,用于定义用户请求的url
from django.conf.urls import url
# 导入当前路径下的views模块 .代表当前路径
from . import views

urlpatterns = [
    # 主页
    url(r"^$", views.IndexView.as_view(), name="index"),
    # sdu清单
    url(r"^list$", views.ListView.as_view(), name="list"),
    # 详情页
    url(r"^detail$", views.DetailView.as_view(), name="detail"),

]
