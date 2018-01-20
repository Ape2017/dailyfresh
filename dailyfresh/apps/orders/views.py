from django.core.urlresolvers import reverse # reverse 逆向解析
# render 返回模板文件 redirect 返回重定向url
from django.shortcuts import render, redirect
# 视图类
from django.views.generic import View
# 自定义组件,限制用户访问权限
from utils.commons import LoginRequiredMixin


class POrderView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'place_order.html')


# 个人中心:所有订单
class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'user_center_order.html')