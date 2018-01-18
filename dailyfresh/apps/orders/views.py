from django.core.urlresolvers import reverse # reverse 逆向解析
# render 返回模板文件 redirect 返回重定向url
from django.shortcuts import render, redirect
# 视图类
from django.views.generic import View
# 自定义组件,限制用户访问权限
from utils.commons import LoginRequiredMixin


class POrder(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'place_order.html')


