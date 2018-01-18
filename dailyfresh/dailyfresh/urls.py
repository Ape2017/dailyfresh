"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import users.urls
import goods.urls

urlpatterns = [
    # 后台用户管理
    url(r'^admin/', include(admin.site.urls)),
    # 用户管理app
    url(r'^users/', include(users.urls, namespace="users")),
    # 商品中心app
    url(r'^', include(goods.urls, namespace="goods")),
    # 购物车app
    url(r'^carts/', include(goods.urls, namespace="carts")),
    # 订单管理app
    url(r'^orders/', include(goods.urls, namespace="orders")),

]

