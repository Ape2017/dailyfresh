# View类视图基础类,用户自定义类视图都是继承此类
from django.views.generic import View
# reverse通过逆向解析字典{模块命名空间:具体请求的 url name} 返回值url
from django.core.urlresolvers import reverse
# 视图中重定向函数,返回指定url到浏览器
from django.shortcuts import redirect
# 视图核心函数,将用户请求数据加载到模板返回到浏览器
from django.shortcuts import render


# 主页视图
class IndexView(View):
    """主页视图"""
    def get(self, request):
        return render(request, 'index.html')


# 商品列表
class ListView(View):
    """商品spu列表"""
    def get(self, request):
        return render(request, 'list.html')


# 商品详情页
class DetailView(View):
    """商品sku详细列表"""
    def get(self, request):
        return render(request, 'detail.html')


