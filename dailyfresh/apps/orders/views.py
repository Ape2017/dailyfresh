"""
    订单视图模块,主要对用户购买行为的管理,如下单,支付,退货等等.
"""
# 视图核心模块,用于返回response对象
from django.shortcuts import render, redirect
# Django自带的视图类
from django.views.generic import View
# 自定义用户登录组件,用于管理用户访问权限
from utils.commons import LoginRequiredMixin
# django中的逆向解析的reverse函数
from django.core.urlresolvers import reverse
# Django中用于管理redis的模块,get_redis_connection用于生成redis数据库对象
from django_redis import get_redis_connection
# 商品应用中模型类GoodsSKU,对应MySQL数据库中sku表
from goods.models import GoodsSKU
# Decimal数据类型,类似浮点数据,用于存储与钱相关关键数据,精度比float高,存储空间比float大
from decimal import Decimal
# 用户模型中的地址类,用于存储用户下单地址
from users.models import Address
# Django自带的JsonResponse类,用于生成Json字符串对象
from django.http import JsonResponse
# 当前应用中模型类,用于存储订单数据
from .models import OrderInfo, OrderGoods
#  django中的时间模块,用于生产订单编号
from django.utils import timezone


# 用户下单视图类
class PlaceOrderView(LoginRequiredMixin, View):
    """确认订单页面"""
    def post(self, request):
        """
        此视图函数是当用户点击购物车页面或商品详情页页面时,所对应的请求
            1.用户下单时,必须登录才能访问此页面,用登录组件LoginRequiredMixin限定
            2.
        :param request: 用户请求对象
        :return: 下单页面对象
        """
        # 一.获取参数
        # 获取的参数有
        # 1.用户对象
        # 2.用户购买的商品id
        # 3.如果是立即购买过来还要有购物数量
        # 获取用户对象
        user = request.user
        # 获取购买商品的商品id列表
        # 列表形式 ['sku_id1','sku_id1','sku_id1',....]
        # 获取多个同名参数的方式getlist,会返回列表
        # 如果是从购物车页面过来,sku_ids中包含所有用户勾选的要下单的商品
        # 如果页面是从商品详情页面过来,sku_ids中保存这个商品的id [sku_id]
        sku_id_list = request.POST.getlist('sku_ids')
        # 如果从详情页面中过来,会包含商品的数量,如果是购物车,将没有数据
        sku_count = request.POST.get('count')

        # 二.校验参数
        # 如果商品列表为None
        if not sku_id_list:
            # 表示参数不完整,, 跳转到购物车页面
            return redirect(reverse('carts:info'))

        # 查询需要的数据,进行校验
        # 获取商品信息,统计信息
        # 初始化数据存储位置
        # skus列表,存储购买商品的sku对象,对象的属性存储需要的数据
        skus = []
        # 初始化小计商品数量
        total_count = 0
        # 初始化商品金额
        total_amount = 0
        # 初始化运费
        trans_cost = 10
        # 获取购物车redis对象
        redis_conn = get_redis_connection('default')
        # 判断请求来至哪里,如果是购物车,sku_count为None
        if not sku_count:
            # 如果从购物车页面过来,查询出用户的购物车中所有的字典
            # 此处cart_dict里的数据是字节类型
            cart_dict = redis_conn.hgetall('cart_%s' % user.id)
            # 遍历商品id列表,校验商品数据
            for sku_id in sku_id_list:
                # 将从POST中取出的sku_id字符串型数据转为字节型
                sku_id = sku_id.encode()
                # 从购物车中判断商品是否存在,获取商品的数量
                if sku_id not in cart_dict:
                    # 购物车不存在这个商品,跳出循环,继续遍历
                    continue
                # 如果购物车中存在该商品,获取数据
                else:
                    # 购买商品的数量
                    sku_count = cart_dict[sku_id]
                    # 从数据库中查询购买商品的信息
                    # 此处要将sku_id的字节型转换成整形或字符串型,上面有转过
                    sku = GoodsSKU.objects.get(id = sku_id.decode())
                    # 将商品数量存储到sku对象的count属性中
                    sku.count = sku_count
                    # 商品的金额
                    # 此处要将sku_count转换成整形再转换成Decimal型
                    # 获取sku对象的价格,根据价格和数量计算出金额
                    sku.amount = sku.price*Decimal(int(sku_count))
                    # 将sku对象添加到skus列表中
                    skus.append(sku)
                    # 根据遍历,获取购买商品的总数量
                    total_count += int(sku_count)
                    # 根据遍历,获取购买商品的总金额
                    total_amount += sku.amount
        else:
            # 如果从立即购买页面过来
            # 遍历商品id列表,校验商品数据
            for sku_id in sku_id_list:
                # 此处sku_id不用转换成字节型,直接时字符串型,字符串型会自动转成数据库中的整形
                sku = GoodsSKU.objects.get(id = sku_id)
                # 将购买数量存入count属性中
                # 此处的sku_count是上面获取参数时的sku_count,是字符串型
                sku.count = sku_count
                # 商品的金额
                # 此处要将sku_count转换成整形再转换成Decimal型
                # 获取sku对象的价格,根据价格和数量计算出金额
                sku.amount = sku.price*Decimal(int(sku_count))
                # 将sku对象添加到skus列表中
                skus.append(sku)
                # 根据遍历,获取购买商品的总数量
                total_count += int(sku_count)
                # 根据遍历,获取购买商品的总金额
                total_amount += sku.amount
                # 将立即购买的商品数据保存到购物车中,顾客点击后反悔,后续可以在购物车中查询
                redis_conn.hset("cart_%s" % user.id, sku_id, sku_count)

        # 查询地址信息
        try:
            # 根据用户获取到最后更新的地址信息
            address = Address.objects.filter(user=user).latest('update_time')
        except Address.DoesNotExist:
            # 如果获取异常,设置为None
            address = None

        # 设置返回的上下文对象
        context = {
            # 地址信息
            'address': address,
            # 购买的商品对象列表
            'skus':skus,
            # 购买商品总件数
            'total_count':total_count,
            # 购买商品的总金额
            'total_amount': total_amount,
            # 运费
            'trans_cost': trans_cost,
            #　最终实付款
            'final_amount': total_amount+trans_cost,
        }
        # 返回加载数据后的模板对象
        return render(request, 'place_order.html',context)


# 订单页面中的提交订单,进入支付流程
class CommitOrderView(View):
    """提交订单 Ajax"""
    def post(self,request):
        """
        提交保存订单
        :param request:
        :return:
        """
        # 判断用户是否属于登录状态,如果未登录,返回Json数据
        # 此处不用LoginRequiredMixin组件是因为请求方式的采用的Ajax
        # Ajax返回值必须是Json字符串数据,二采用LoginRequiredMixin组件返回的是重定向的页面
        # 判断用户是否是登录状态
        if not request.user.is_authenticated():
            # 用户未登录,返回Json数据字符串,告知前端页面
            return JsonResponse({'code':1,'errmsg':'用户未登录'})
        # 获取参数
        # 用户是登录状态,获取用户对象
        user = request.user
        # 获取支付时必须的参数,将参数存储到数据库中
        # 获取参数 收货地址 address_id,支付方式编号,商品sku_id,商品数量
        # 根据sku_id获取购物车中该商品的数量
        address_id = request.POST.get('address_id')
        # 获取支付方式
        pay_method = request.POST.get('pay_mehtod')
        # 获取商品对象id的字符串
        # "1,2,3,4"
        sku_ids_str = request.POST.get('sku_ids')
        # 获取用户的购物车数据
        # 生成购物车对象
        redis_conn = get_redis_connection("default")
        # 获取用户购物车数据
        cart_dict = redis_conn.hgetall('cart_%s' % user.id)

        # 校验参数
        # 判断参数的完整性,如果有一个参数为None,说明参数不完整,返回提示信息到前端
        if not all([address_id,pay_method,sku_ids_str]):
            return JsonResponse({'code':2,'errmsg':'参数不完整'})
        # 判断地址信息的有效性
        try:
            # 此处address_id是字符串类型,系统会自动转成int型
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            # 若获取失败,返回异常信息
            return JsonResponse({'code':3,'errmsg':'收货地址信息有误'})
        # 判断支付方式是否存在
        if pay_method not in OrderInfo.PAY_METHOD.keys():
            # 若获取失败,返回异常信息
            return JsonResponse({'code':4,'errmsg':'不支持的支付方式'})

        # 构建数据,用于存储到数据库中
        # 构建订单编号 20180123153535用户id
        # 时间戳
        # order_id ="%d%06d" % (int(time.time()), user.id)
        # 获取时间字符串
        # strftime 将时间转成字符串
        # strptime 将字符串转成时间
        # %Y%m%d%H%M%S Y表示年m表示月d表示天H表示24小时M表示分S表示秒
        time_str = timezone.now().strftime("%Y%m%d%H%M%S")
        # 生成订单号
        order_id = "%s%06d" % (time_str,user.id)
        # 创建订单基本信息表数据,用于存储到数据库
        order = OrderInfo.objects.create(
            order_id = order_id,
            user = user,
            address =address,
            total_count = 0,
            total_amount = 0,
            trans_cost=Decimal("10.0"),
            pay_method = pay_method
        )
        # 初始化购买商品数量,用于下面计算
        total_count = 0
        # 初始化购买商品数量,用于下面计算
        total_amount = 0
        # 获取商品id的列表,将存储商品id的字符串分割成列表
        # ["1","2","3"...]
        sku_ids_list = sku_ids_str.split(",")
        # 校验商品id的有效性,获取商品信息,保存订单信息
        for sku_id in sku_ids_list:
            try:
                # 获取商品sku对象
                sku = GoodsSKU.objects.get(id = sku_id)
            except GoodsSKU.DoesNotExist:
                # 出现异常,说明商品id不在数据库中
                # 返回异常信息
                return JsonResponse({'code': 5, 'errmsg': '商品信息有误'})
            # 获取购物车中该商品存储的数量
            # 此处sku_id为字符串型,要转成字节型
            count = cart_dict.get(sku_id.encode())
            # 获取该商品购买数量的字节型,用int()转成整形
            count = int(count)
            # 判断库存
            if count > sku.stock:
                # 超过库存,返回异常信息
                return JsonResponse({'code': 6, 'errmsg': '用户未登录'})
            # 构建订单表中数据,用于存储到数据库中
            OrderGoods.objects.create(
                order=order,
                sku=sku,
                count=count,
                price=sku.price,
            )
            # 商品库存与销量处理
            # 商品中的库存减去购买数量
            sku.stock -= count
            # 商品中的销量增加购买数量
            sku.sales += count
            # 保存sku更新后的数据
            sku.save()
            # 购买商品的总数量,每次循环加一次
            total_count += count
            # 购买商品的总金额,每次循环加一次
            total_amount += (sku.price*Decimal(count))
        # 在订单表中的保存总金额和总购物数量
        # total_count是for循环遍历后的总数量结果
        order.total_count = total_count
        # total_amount是for循环遍历后的总金额结果
        order.total_amount = total_amount
        # 保存订单数据
        order.save()
        # 移除购物车的数据
        # redis_conn.hdel("cart_%s" % user.id, 1,2,3,4,5)
        # hdel可以删除多个键值对,hdel(self ,name ,*keys)
        # *sku_ids_list是拆包
        redis_conn.hdel('cart_%s' % user.id, *sku_ids_list)

        #返回Json数据
        return JsonResponse({'code': 0, 'errmsg': '保存成功'})


# 个人中心:所有订单
class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'user_center_order.html')