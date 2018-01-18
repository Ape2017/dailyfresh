from django.shortcuts import render # render返回模板文件
# View系统默认类视图
from django.views.generic import View
# 自定义组件,限制用户访问权限,登陆状态:允许访问 未登陆状态:跳转到主页
from utils.commons import LoginRequiredMixin


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'cart.html')