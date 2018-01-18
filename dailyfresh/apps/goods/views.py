from django.shortcuts import render
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


# 主页视图
class IndexView(View):
    """主页视图"""
    def get(self, request):
        return render(request, 'index.html')


# 商品列表
class ListView(View):
    def get(self, request):
        return render(request, 'list.html')


# 商品详情页
class DetailView(View):
    def get(self, request):
        return render(request, 'detail.html')


