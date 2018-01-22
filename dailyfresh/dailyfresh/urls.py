"""
dailyfresh URL Configuration
dailyfresh URL配置
The `urlpatterns` list routes URLs to views. For more information please see:
“urlpatterns”列表将URL路由到视图。 欲了解更多信息，请参阅：
https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
例如:
Function views
基于函数的视图
    1. Add an import:  from my_app import views
    1.添加一个导入：从my_app导入视图
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
    2.向urlpatterns添加一个URL：url（r'^ $'，views.home，name ='home'）
Class-based views
基于类的视图
    1. Add an import:  from other_app.views import Home
    1.添加一个import：from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
    2.向urlpatterns添加一个URL：url（r'^ $'，Home.as_view（），name ='home'）
Including another URLconf
包含url的配置
    1. Add an import:  from blog import urls as blog_urls
    1.添加一个导入：从blog应用导入URL作为blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
    2.向urlpatterns添加一个URL：url（r'^ blog /'，include（blog_urls））
"""
# Django配置模块 include包含函数 url路由
from django.conf.urls import include, url
# 普通核心模块
from django.contrib import admin
# 全文检索
from haystack import urls as haystackurls
# 富文本编辑器模块
from tinymce import urls as tinymceurls
# 用户应用
from users import urls as usersurls
# 商品应用
from goods import urls  as goodsurls
# 购物车
from carts import urls as cartsurls
# 订单管理
from orders import urls as ordersurls

urlpatterns = [
    # 后台用户管理
    url(r'^admin/', include(admin.site.urls)),
    # 富文本编辑器
    url(r'^tinymce/', include(tinymceurls)),
    # 全文检索
    url(r'^search/',include(haystackurls)),
    # 用户管理app
    url(r'^users/', include(usersurls, namespace="users")),
    # 商品中心app
    url(r'^', include(goodsurls, namespace="goods")),
    # 购物车app
    url(r'^carts/', include(cartsurls, namespace="carts")),
    # 订单管理app
    url(r'^orders/', include(ordersurls, namespace="orders")),

]

