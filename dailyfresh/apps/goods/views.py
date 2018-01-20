# View类视图基础类,用户自定义类视图都是继承此类
from django.views.generic import View
# reverse通过逆向解析字典{模块命名空间:具体请求的 url name} 返回值url
from django.core.urlresolvers import reverse
# 视图中重定向函数,返回指定url到浏览器
from django.shortcuts import redirect
# 视图核心函数,将用户请求数据加载到模板返回到浏览器
from django.shortcuts import render
# 商品类别表
from dailyfresh import settings
from .models import GoodsCategory
# 商品SPU表
from .models import Goods
# 商品SKU表
from .models import GoodsSKU
# 商品图片
from .models import GoodsImage
# 主页轮播商品展示
from .models import IndexGoodsBanner
# 主页分类商品展示,枚举
from .models import IndexCategoryGoodsBanner
# 主页促销活动展示
from .models import IndexPromotionBanner


# 主页视图
class IndexView(View):
    """主页视图"""
    def get(self, request):
        # 方法一:不使用页面静态化处理,直接给用户返回加载动态数据后的页面
        # # 商品的品类
        # categories = GoodsCategory.objects.all()
        # # 首页轮播图
        # index_goods_banners = IndexGoodsBanner.objects.all()[:4]
        # # 首页广告活动数据,[]切片,限制数量
        # promotion_banners = IndexPromotionBanner.objects.all()[:2]
        # # 首页分类商品展示数据
        # for category in categories:
        #     category_goods_title_banners = IndexCategoryGoodsBanner.objects.filter(category=category,
        #     display_type = 0).order_by(category.index)[:5]
        #     category.title_banners = category_goods_title_banners
        #     category_goods_image_banners = IndexCategoryGoodsBanner.objects.filter(category=category,
        #     display_type = 1).order_by(category.index)[:4]
        #     category.image_banners = category_goods_image_banners
        # print只接受字符串,当传入对象时,对象会先去调用__str__方法,返回字符串
        #     print(category.title_banners)
        #     print(category.image_banners )
        #     print(category)
        #     print('')
        # # 购物车数量
        # cart_num = 0
        # # 模板的数据
        # context = {
        #     'categories': categories,
        #     'index_goods_banners': index_goods_banners,
        #     'promotion_banners': promotion_banners,
        #     'cart_num': cart_num,
        # }
        # print("context")
        # print(context)
        # # context数据内容有:
        # #     {
        # #         'categories': categories,
        # #         'index_goods_banners': index_goods_banners,
        # #         'promotion_banners': promotion_banners,
        # #         'cart_num': cart_num,
        # #     }
        # return render(request, 'index.html', context)
        # 方法二:采用页面静态化处理,可以优化用户访问时间和降低数据库操作以及服务器压力
        # 页面静态化步骤:
            # 1.运营人员操作admin录入商品数据
            # 2.Django将存储任务发布到celery任务队列中
            # 3.在Celery处理admin站点保存请求的时候,执行生成静态页面的任务
            # 4.将生成的静态页面保存到fastDFS服务器中(Nginx)
            # 5.将地址返回到Django中
        url = settings.FASTDFS_NGINX_URL+'stctic/index.html'
        return redirect(url)


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


