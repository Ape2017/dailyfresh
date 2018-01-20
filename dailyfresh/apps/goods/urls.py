# django核心模块中的url,用于定义用户请求的url
from django.conf.urls import url
# 导入当前路径下的views模块 .代表当前路径
from . import views

urlpatterns = [
    # 主页
    # 动态主页,使用缓存,静态主页由nginx返回
    url(r"^index$", views.IndexView.as_view(), name="index"),
    # sdu清单
    url(r"^list$", views.ListView.as_view(), name="list"),
    # 详情页(?P<sku_id>\d+)中?P<sku_id>表示起别名 \d+表示数字
    url(r"^detail/(?P<sku_id>\d+)$", views.DetailView.as_view(), name="detail"),

]
