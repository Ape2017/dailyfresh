"""
商品应用中的视图模块
    1.处理用户的url请求
    2.操作数据库,对数据库进行增删改查
    3.获取数据后加载到模板文件返回到浏览器
视图类的逻辑处理思路:
    1.分析用户行为,判断请求方式
    2.通过请求模式,判断返回的html页面
    3.分析html页面,提取返回数据
    4.根据提取出的数据,结合html页面生成模板文件
    5.获取用户请求的参数
    6.校验参数的有效性
    6.查询数据库
    7.数据处理
    8.返回数据
"""
from django.views.generic import View  # View类视图基础类,用户自定义类视图都是继承此类
# reverse通过逆向解析字典{模块命名空间:具体请求的 url name} 返回值url
from django.core.urlresolvers import reverse
# 视图中重定向函数,返回指定url到浏览器
from django.shortcuts import redirect
# 视图核心函数,将用户请求数据加载到模板返回到浏览器
from django.shortcuts import render
# 商品类别表
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
# 系统缓存机制
from django.core.cache import cache
# 首页缓存有效期,详情页缓存有效期
from utils.constants import INDEX_DATA_CACHE, DETAIL_DATA_CACHE_EXPIRES
# 引入商品的评论数据,通过订单商品查询
from orders.models import OrderGoods
# 用户浏览记录存入redis
from django_redis import get_redis_connection
# 分页器
from django.core.paginator import Paginator, EmptyPage
# 导入Json
import json


# 获取购物车数量的公用类
class BaseCartView(View):
    """自定义的保存了求取购物车数量的方法的视图父类"""

    # 定义获取购物车数量的方法
    def get_cart_num(self, request):
        """
        获取用户购物车数量
        :param self:类实例对象
        :param request: 用户的请求,用于获取参数
        :return: 返回购物里商品的总数
        """
        # 判断用户是否登录,
        # 登录状态从redis数据库中获取数据
        # 未登录状态从cookie中获取数据
        if request.user.is_authenticated():
            user = request.user
            # 从redis中获取所有购物车信息
            # 获取redis对象,即setting文件中redis的default对应的数据库
            redis_coon = get_redis_connection('default')
            # 通过hgetall方法获取用户购物车的所有数据
            cart_dict = redis_coon.hgetall("cart_%s" % user.id)
            # 定义购物车的初始值
            cart_num = 0
            # 遍历cart_dict的values值
            for val in cart_dict.values():
                cart_num += int(val)
            # 返回购物车数据
            return cart_num
        else:
            # 如果用户未登录,从cookie中获取值
            # cookie中存储的是字符串类型
            cart_json_str = request.COOKIES.get('cart_info')

            if cart_json_str:
                # cookie里有购物车数据
                cart_dict = json.loads(cart_json_str)

                cart_num = 0

                for val in cart_dict.values():
                    cart_num += int(val)

                return cart_num
            else:
                return 0


# 主页视图
class IndexView(BaseCartView):
    """主页视图"""
    # /index
    def get(self, request):
        # 方法一:不使用页面静态化处理和缓存机制,直接将数据库中查询到的数据加载到模板中返回给浏览器
        # 缺点:1.导致用户每一次请求都会操作数据库,会加大数据库服务器的压力
        #     2.数据库压力过大会导致响应用户请求慢,导致用户体验差
        # 实现逻辑
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
        #     'categories': categories,# categories对象列表
        #     'index_goods_banners': index_goods_banners,# 列表
        #     'promotion_banners': promotion_banners,
        #     'cart_num': cart_num,
        # }
        # print("context")
        # print(context)
        # context中的数据内容为{
        #     "categorires": [category_obj, category_obj, ....](对象列表 )
        #     "index_goods_banners": []
        #     "promotion_banners": []
        #     "cart_num": 0
        # }
        # 其中:category_obj对象的属性有{
        # name,
        # logo,
        # image,
        # title_banners->[ IndexCategoryGoodsBanner_obj, IndexCategoryGoodsBanner_obj .. ]
        # image_banners->[ IndexCategoryGoodsBanner_obj, IndexCategoryGoodsBanner_obj, ...]
        #   }
        # return render(request, 'index.html', context)

        # 方法二:采用页面静态化处理,将低频数据的动态页面转化为静态页面存储到Nginx服务
        # 优点:能够优化用户访问时间和降低数据库操作
        # 缺点:用户访问高频数据或个性化数据时,还是要大量操作数据库,会导致数据库压力
        # 页面静态化步骤:
        # 1.运营人员操作admin录入商品数据
        # 2.Django将存储任务发布到celery任务队列中
        # 3.在Celery处理admin站点保存请求的时候,执行生成静态页面的任务
        # 4.将生成的静态页面保存到fastDFS服务器中(Nginx)
        # 5.将地址返回到Django中
        # 代码实现:
        #       1.在celery_task/task.py模块中设计发布/执行时对应的celery任务
        #       2.在当前app下的admin.py模块中注册发布celery任务的入口
        #       3.启动celery服务器
        #       4.修改对应的Nginx服务器的配置文件,并且启动服务器
        #       5.celery执行任务生成静态页面存储到指定的路径下(在celery_task/task.py中)

        # 方法三:采用缓存机制 redis
        # 优点:将高频常用数据加入到缓存中后,能够提高用户体验
        # 缺点:缓存如果没有设置有效期,将会导致缓存和数据库的数据不同步
        # context尝试从缓存中获取缓存数据
        context = cache.get('index_data')
        print('缓存的数据')
        print(context)
        # 判断缓存是否存在
        if context is None:
            # 没有缓存数据，需要查询数据库
            print("进行了数据库的查询")
            # 商品的品类
            categories = GoodsCategory.objects.all()
            print('商品的分类')
            print(categories)
            # 首页轮播图
            index_goods_banners = IndexGoodsBanner.objects.all().order_by("index")[:4]
            print('幻灯片图')
            print(index_goods_banners)
            # 首页广告活动数据,[]切片,限制数量
            promotion_banners = IndexPromotionBanner.objects.all().order_by("index")[:2]
            # 广告图片
            print('广告')
            print(promotion_banners)
            # 首页分类商品展示数据
            for category in categories:
                category_goods_title_banners = \
                    IndexCategoryGoodsBanner.objects.filter(category=category,display_type=0).order_by('index')[:5]
                # python的特性：可以向对象中添加新的属性，通过属性赋值的方式
                # 在title_banners对象中增加image_banners属性
                category.title_banners = category_goods_title_banners
                print('首页分类商品中展示的商品名称')
                print(category_goods_title_banners)
                category_goods_image_banners = \
                    IndexCategoryGoodsBanner.objects.filter(category=category,display_type=1).order_by('index')[:4]
                # 在category对象中增加image_banners属性
                # python的特性：可以向对象中添加新的属性，通过属性赋值的方式
                category.image_banners = category_goods_image_banners
                print('首页分类商品中展示的商品名称')
                print(category_goods_image_banners)

            # 购物车数量
            cart_num = self.get_cart_num(request)
            print('购物车数量')
            print(cart_num)

            # 模板的数据
            context = {
                'cart_num': cart_num,
                'categories': categories,
                'index_goods_banners': index_goods_banners,
                'promotion_banners': promotion_banners,
            }
            print('组合后的模板数据')
            print(context)
            # 使用django的cache工具保存缓存数据
            # cache.set(名字,数据,有效期)
            cache.set('index_data', context, INDEX_DATA_CACHE)

        # 数据加载到模板,生成html,返回到浏览器
        return render(request, 'index.html', context)


# 商品详情页
class DetailView(BaseCartView):
    """商品sku详细列表"""
    # GET的两种传参方式 /detail/1 或 /detail?sku_id = 1
    def get(self, request, sku_id):
        """
        提供详情页页面
        :param request: 用户请求的url
        :param sku_id: 传入具体的商品id
        :return:
        """
        # 尝试获取缓存数据
        context = cache.get('"detail_%s" % sku_id')
        # 如果缓存里面没有数据,查询数据库
        if context is None:
            # 商品分类信息
            categories = GoodsCategory.objects.all()
            # 取出sku的数据对象
            try:
                sku = GoodsSKU.objects.get(id=sku_id)
            except GoodsSKU.DoesNotExist:
                return redirect(reverse('goods:index'))
            # 相同的spu的其他sku数据
            spu = sku.goods
            # other_skus = spu.goodssku_set.exclude(id=sku.id)
            other_skus = spu.goodssku_set.exclude(id=sku_id)
            # 新品推荐
            new_skus = GoodsSKU.objects.filter(category=sku.category).order_by('-create_time')[:2]
            # 评论数据
            order_goods_list = OrderGoods.objects.filter(sku=sku).exclude(comment='').order_by('-update_time')[:30]
            # 组装模板数据
            context = {
                'categories': categories,
                'sku': sku,
                'other_skus': other_skus,
                'new_skus': new_skus,
                'order_goods_list': order_goods_list,
            }
            # 购物车数据
            cart_num = self.get_cart_num(request)
            context['cart_num'] = cart_num
            # 将数据保存到缓存中
            cache.set('detail_%s' % sku_id, context, DETAIL_DATA_CACHE_EXPIRES)
            # 保存用户浏览记录
            # 获取用户对象
            user = request.user
            # 判断用户是否登录
            # 如果用户时登录状态
            if user.is_authenticated():
                # 获取redis数据库对象
                redis_conn = get_redis_connection("default")
                # 移除浏览器历史中的相同记录
                redis_conn.lrem("history_%s" % user.id, 0, sku_id)
                # redis对象调用方法将数据存入数据库中,添加用户的浏览历史记录
                redis_conn.lpush('history_%s' % user.id, sku_id)
                # 取出超过数量的记录,只显示五条
                redis_conn.ltrim('history_%s' % user.id, 0, 4)

        # 将数据加载到模板返回数据
        return render(request, 'detail.html', context)


# 分类商品列表
class ListView(BaseCartView):
    """商品spu列表"""
    # url 定义GET/list/(category_id)/(page)?sort = xxxx
    def get(self, request, category_id, page):
        """提供页面 商品类别、排序、页数"""
        # 尝试获取缓存数据
        context = cache.get("'category_%s' % category_id")
        # 如果缓存不存在
        if context is None:
            # 1.设置排序参数
            # 其中get为Python字典中的get函数
            # Python 字典(Dictionary) get() 函数返回指定键的值，如果值不在字典中返回默认值。
            # get语法:dict.get(key, default=None)
            # 参数1:key -- 字典中要查找的键。
            # 参数2:default关键字参数 -- 如果指定键的值不存在时，返回该默认值值。
            # 返回值:返回指定键的值，如果值不在字典中返回默认值None。
            # 设置排序参数,下面会使用,自定义为default,
            sort = request.GET.get('sort', 'default')
            # 2.校验参数的合法性
            # 判断类别是否存在
            try:
                category = GoodsCategory.objects.get(id=category_id)
            except GoodsCategory.DoesNotExist:
                return redirect(reverse('goods:index'))
            # 查询数据库
            # 购物车
            cart_num = self.get_cart_num(request)
            # 所有商品类别
            categories = GoodsCategory.objects.all()
            # 新品推荐
            new_skus = GoodsSKU.objects.filter(category=category).order_by('-create_time')[:2]
            # 获取商品列表数据
            if sort == 'price':
                skus = GoodsSKU.objects.filter(category=category).order_by('price')
            elif sort == 'hot':
                skus = GoodsSKU.objects.filter(category=category).order_by('-sales')
            else:
                skus = GoodsSKU.objects.filter(category=category).order_by("-create_time")
            # 分页器
            # 创建分页器对象paginator
            # paginator = Paginator(要进行分页处理的所有数据,每页数量)
            paginator = Paginator(skus, 1)

            # 获取当前页的数据,前端传过来的page数据是字符串
            page = int(page)
            try:
                page_skus = paginator.page(page)
            except EmptyPage:
                # 表示page的页数不在分页处理之后的页数之内,属于非法的页数请求
                page = 1
                page_skus = paginator.page(page)

            # 自己控制页码的展示
            # 计算页码的范围
            # 获取总页数
            num_pages = paginator.num_pages
            # 总页数小于5页
            if num_pages < 5:
                page_nums = list(range(1, num_pages + 1))
            # 总页数大于5页,当前页属于前3页
            elif page <= 3:
                page_nums = [1, 2, 3, 4, 5]
                page_nums = list(range(1, 6))

            # 总页数大于5页,当前页属于最后3页
            elif page >= (num_pages - 2):
                page_nums = list(range(num_pages - 4, num_pages + 1))
            # 其他
            else:
                page_nums = list(range(page - 2, page + 3))

            context = {
                'catr_num': cart_num,
                'category': category,
                'categories': categories,
                'new_skus': new_skus,
                'page_skus': page_skus,
                'page_nums': page_nums,
                'sort': sort,
            }

            cache.set('category_%s' % category_id, context, DETAIL_DATA_CACHE_EXPIRES)

        # 返回渲染页面
        return render(request, 'list.html', context)
