"""
    订单视图模块,主要对用户购买行为的管理,如下单,支付,退货等等.
"""
# 视图核心模块,用于返回response对象
import time
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
# 添加事务自定义组件,用于告诉系统使用自定义的事务管理
from utils.commons import TransactionAtomicMixin
# 数据库事务组件,用于设置事务保存点
from django.db import transaction
# 分页器
from django.core.paginator import Paginator
# 支付宝
from alipay import AliPay
# 配置文件
from dailyfresh import settings
# 操作系统
import os
# Django中的缓存对象
from django.core.cache import cache


# 用户下单
class PlaceOrderView(LoginRequiredMixin, View):
    """确认订单页面"""
    def post(self, request):
        """
        此视图函数是当用户点击购物车页面或商品详情页页面时,所对应的请求
            1.用户下单时,必须登录才能访问此页面,用登录组件LoginRequiredMixin限定
            2.来源有立即购买和购物车
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
            # 最终实付款
            'final_amount': total_amount+trans_cost,
            # 渲染到模板中,用于传到提交页面
            'sku_ids': ",".join(sku_id_list)
        }
        # 返回加载数据后的模板对象
        return render(request, 'place_order.html',context)


# 提交订单,进入支付流程
class CommitOrderView(TransactionAtomicMixin,View):
    """提交订单 Ajax"""
    def post(self,request):
        """
        提交保存订单,进入支付界面
        :param request:请求对象,来自Ajax的post请求
        :return:返回Json数据字符串
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

        # 创建事务的保存点,记录数据库的初始化状态
        save_id = transaction.savepoint(())

        try:
            # 创建订单基本信息表数据,存储到数据库
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address,
                total_count=0,
                total_amount=0,
                trans_cost=Decimal("10.0"),
                pay_method=pay_method
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
                # 尝试三次
                for i in  range(3):
                    try:
                        # 获取商品sku对象
                        sku = GoodsSKU.objects.get(id = sku_id)
                    except GoodsSKU.DoesNotExist:
                        # 出现异常,说明商品id不在数据库中
                        # 返回异常信息
                        # 出现异常,回滚到保存点,即撤销之前的所有操作,
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'code': 5, 'errmsg': '商品信息有误'})
                    # 获取购物车中该商品存储的数量
                    # 此处sku_id为字符串型,要转成字节型
                    count = cart_dict.get(sku_id.encode())
                    # 获取该商品购买数量的字节型,用int()转成整形
                    count = int(count)

                    # 判断库存
                    if count > sku.stock:
                        # 超过库存,返回异常信息
                        # 出现异常,回滚到保存点,即撤销之前对数据库的所有操作
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'code': 6, 'errmsg': '用户未登录'})

                    # 此处没有处理并发库存管理,会导致数据库操作异常
                    # 商品库存与销量处理
                    # 商品中的库存减去购买数量
                    # sku.stock -= count
                    # # 商品中的销量增加购买数量
                    # sku.sales += count
                    # # 保存sku更新后的数据
                    # sku.save()
                    # 处理并发库存管理的方法有:
                    # 1.悲观锁,会出现死锁,性能降低
                    # 2.乐观锁,不会出现死锁,性能降低最少
                    # 3.任务队列,类似悲观锁,没有死锁
                    # 使用乐观锁的方式,解决并发更新库存的问题
                    # 原始库存
                    origin_stock = sku.stock
                    # 新库存
                    new_stock = origin_stock - count
                    # 新销量
                    new_sales = sku.sales + count
                    # update返回成功更新的行数,成功更新1,不成功0
                    result =GoodsSKU.objects.filter(id=sku.id, stock=origin_stock)\
                        .update(stock=new_stock,sales=new_sales)
                    # 判断是否更新成功
                    if result == 0 and i<2:# 前两次循环尝试
                        # 表示更新不成功
                        continue
                    elif request == 0 and i ==2: # 第三次循环 尝试
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'code': 8, 'errmsg': '订单保存不成功'})
                    # 表示更新库存成功
                    # 构建订单表中数据,存储到数据库中
                    OrderGoods.objects.create(
                        order=order,
                        sku=sku,
                        count=count,
                        price=sku.price,
                    )
                    # 购买商品的总数量,每次循环加一次
                    total_count += count
                    # 购买商品的总金额,每次循环加一次
                    total_amount += (sku.price*Decimal(count))
                    # 结束这个商品的尝试,处理下一个商品
                    break
            # 在订单表中的保存总金额和总购物数量
            # total_count是for循环遍历后的总数量结果
            order.total_count = total_count
            # total_amount是for循环遍历后的总金额结果
            order.total_amount = total_amount+Decimal("10.0")
            # 保存订单数据
            order.save()
        except Exception:
            # 出现了其他的任何异常,都要回滚到保存点
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'code': 7, 'errmsg': '数据库异常'})

        # 提交事务
        # 事务保存提交,表示从保存点之后的所有操作
        transaction.savepoint_commit(save_id)

        # 移除购物车的数据
        # redis_conn.hdel("cart_%s" % user.id, 1,2,3,4,5)
        # hdel可以删除多个键值对,hdel(self ,name ,*keys)
        # *sku_ids_list是拆包
        redis_conn.hdel('cart_%s' % user.id, *sku_ids_list)

        #返回Json数据
        return JsonResponse({'code': 0, 'errmsg': '保存成功'})


# 个人中心:订单
class UserOrdersView(LoginRequiredMixin, View):
    def get(self, request,page):
        # 获取用户
        user = request.user
        # 查询订单
        orders = user.orderinfo_set.all().order_by('-create_time')

        for order in orders:
            order.status_name = OrderInfo.ORDER_STATUS[order.status]
            order.pay_method_name = OrderInfo.PAY_METHOD[order.pay_method]
            order.skus = []
            order_skus = order.ordergoods_ser.all()
            for order_sku in order_skus:
                sku = order_sku.sku
                sku.count = order_sku.count
                sku.amount = sku.price * Decimal(sku.count)
                order.skus.append(sku)

        # 分页
        paginator = Paginator(orders, 3)

        # 获取页码的列表
        pages = paginator.page_range

        # 获取总页数
        num_pages = paginator.num_pages

        # 当前页转化为数字
        page = int(page)

        # 1.如果总页数<=5
        # 2.如果当前页是前3页
        # 3.如果当前页是后3页
        # 4.既不是前3页,也不是后三页
        if num_pages <= 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1,6)
        elif (num_pages - page) <=2:
            pages = range(page -2, page +3 )

        # 获取page页的内容 has_previous has_next number
        page_orders = paginator.page(page)

        context = {
            'orders':page_orders,
            'page': page,
            'pages':pages,
        }

        return render(request, 'user_center_order.html', context)


# 商品评论
class CommentView(LoginRequiredMixin,View):
    """
        此视图类处理的是商品评论信息的获取和上传,其中获取是get方式
        上传post方式
    """
    def get(self,request,order_id):
        """
        用户获取商品评论信息,通过order_id获取信息,其中order_id是通过url位置进行传传递参数
        :param request: 用户请求对象
        :param order_id: 商品订单id
        :return: 返回页面对象
        """
        # 提供评论页面
        # 用户已经通过LoginRequiredMixin验证过,不要判断,直接获取
        user = request.user
        # 判断order是否存在
        try:
            # 根据order_id和user获取订单对象
            order = OrderInfo.objects.get(order_id=order_id,user=user)
        # 出现异常,没有找到,重定向到订单信息页面
        except OrderInfo.DoesNotExist:
            # 返回重定向的页面对象
            return redirect(reverse("orders:info"))
        # 获取订单状态信息
        order.status_name = OrderInfo.ORDER_STATUS[order.status]
        # 初始化订单商品对象,用list存储
        order.skus = []
        # 查询出所有的order_sku对象
        order_skus = order.ordergoods_set.all()
        # 遍历order_skus对象,获取每一个order_sku
        for order_sku in order_skus:
            # 获取商品对象,通过order_sku的外键sku获取
            sku = order_sku.sku
            # 获取订单商品对象的个数
            sku.count = order_sku.count
            # 获取商品的金额
            # 因为价格的数据类型是Decimal,所以count也要转成Decimal类型
            sku.amount = order_sku.price * Decimal(sku.count)
            # 逐一添加到skus列表中
            order.skus.append(sku)
        # 返回页面对象到Django
        return render(request, "order_comment.html", {"order": order})

    def post(self,request,order_id):
        """
        通过表单上传,post方式
        用户上传商品评论信息,通过order_id获取信息,其中order_id是通过url位置进行传传递参数
        :param request: 用户请求对象
        :param order_id: 订单编号
        :return: 重定向到订单info页面
        """
        # 获取用户对象，通过LoginRequiredMixin限制用户访问权限
        user = request.user
        # 获取订单
        try:
            # 通过订单编号获取和用户在订单信息表中查询订单对象
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        # 表示没有查询到订单信息
        except OrderInfo.DoesNotExist:
            # 直接重定向到订单信息页面
            return redirect(reverse("orders:info"))

        # 获取评论条数,通过POST属性获取,返回的是字符串
        total_count = request.POST.get("total_count")
        # 将字符串转成整形
        total_count = int(total_count)
        # 通过遍历1到商品数量的+1的数,获取每一个整数
        for i in range(1, total_count + 1):
            # 获取前端表单传来的sku_id
            # 这里是自定义的sku_id,不是实际的sku_id
            # 是前端中form表单中的input输入框中的name属性
            sku_id = request.POST.get("sku_%d" % i)
            # content是前端传来的每一个评论信息的value
            # 此处通过给要评论的商品进行同一自定义编号,
            # 比如sku_1对应1号商品,content_1代表1号商品的评论
            content = request.POST.get('content_%d' % i, '')
            try:
                # 获取订单商品对象,根据订单和商品编号获取
                order_goods = OrderGoods.objects.get(order=order, sku_id=sku_id)
            # 如果获取不成功就或下一个商品的评论信息
            except OrderGoods.DoesNotExist:
                # 继续下一次获取
                continue
            # 将评论信息保存到order_goods表中
            order_goods.comment = content
            # 提交保存
            order_goods.save()

            # 清除商品详情缓存,因为之前该商品详情页有设置缓存,现在更改了评论要清楚缓存
            cache.delete("detail_%s" % sku_id)
        # 所有商品的评论更新成功后,将订单的status表示改为已完成
        order.status = OrderInfo.ORDER_STATUS_ENUM["FINISHED"]
        # 提交保存
        order.save()
        # 重定向到个人中心页面
        return redirect(reverse("orders:info", kwargs={"page": 1}))


# 发起支付页面
class PayView(View):
    """
        由个人中心,个人订单中的去支付按钮中定义的Ajax发起,
        主要功能是用户发起请求调起支付宝支付页面
        方式: Ajax的post请求
        路径: /orders/pay
    """
    def post(self,request):
        """
        功能:在用户浏览器中打开支付宝支付页面
        :param request: 用户请求对象
        :return: Json数据对象
        """
        # 判断用户的登录状态
        # 判断用户的登录状态,此处用is_authenticated是因为返回的是Json对象,而不是Response对象
        if not request.user.is_authenticated():
            # 用户未登录,返回错误信息到Ajax,Ajax再根据code的值进行判断
            return JsonResponse({"code":1,"errmsg":"用户未登录"})
        # 获取数据 订单编号 若没有返回None
        order_id = request.POST.get('order_id')
        # 校验参数
        if not order_id:
            # 没有订单编号,返回错误信息到Ajax,Ajax再根据code的值进行判断
            return JsonResponse({"code":2,"errmsg":"参数有误"})
        # 获取用户对象,此处在上面已经判断
        user = request.user
        # 判断订单时是否存在
        try:
            # 获取订单对象,根据order_id(订单号),user(用户),status(状态),pay_method支付方式
            order = OrderInfo.objects.get(order_id=order_id,
                                      user=user,
                                      status=OrderInfo.ORDER_STATUS_ENUM["UNPAID"],
                                    pay_method=OrderInfo.PAY_METHODS_ENUM['ALIPAY'])
        # 出现异常,表示没找到
        except OrderInfo.DoesNotExist:
            # 没有订单编号,返回错误信息到Ajax,Ajax再根据code的值进行判断
            return JsonResponse({"code":3,"errmsg":"订单信息有误"})
        # 订单获取成功,向支付宝发起支付请求,获取支付参数
        # 创建支付宝支付客户端对象
        alipay_client = AliPay(
            # 支付宝支付应用id,在支付宝沙箱位置
            appid=settings.ALIPAY_APPID,
            # 支付完成跳转回的链接地址
            app_notify_url=None,
            # 私钥,用户生成,公钥在支付宝端已经配置好
            app_private_key_path=os.path.join(settings.BASE_DIR, "apps/orders/keys/app_private_key.pem"),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(settings.BASE_DIR, "apps/orders/keys/alipay_public_key.pem"),
            # 加密方式 RSA 或者 RSA2
            sign_type = "RSA2",
            # 默认False, 如果是True，表示使用沙箱环境
            debug = True,
        )
        # 使用工具对象,发起电脑支付请求
        # 通过使用支付宝支付客户端调用api_alipay_trade_app_pay支付函数,生成一个支付链接的后半部分
        # 参数在order_string中存储,返回加密的字符串
        order_string = alipay_client.api_alipay_trade_app_pay(
            # 订单编号
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject='tiantianshengxian %s' % order_id,
            return_url=None,
            notify_url=None,
        )
        # 构建用户访问的支付宝支付网址
        # 此url为Ajax打开新窗口请求的url,是通过向支付宝发送请求
        # ALIPAY_GATEWAY为支付宝支付网关网址
        # "?"表示是通过get方式传递参数 其中get参数形式的url为 .xxx?a=1&b=2
        alipay_url = settings.ALIPAY_GATEWAY+"?"+order_string
        # 返回确认信息到Ajax,Ajax再根据code的值进行判断
        return JsonResponse({"code": 0, "errmsg": "成功","pay_url": alipay_url})


# 查询支付结果
class CheckPayResultView(View):
    """
    查询用户支付订单的结果
    请求方式:
        Ajax:GET /orders/check_pay?order_id=xxxx
    """
    def get(self,request):
        """
        通过get方式传递参数,查询用户支付结果
        :param request: 请求对象
        :return: Json返回对象
        """
        # 判断用户的登录状态,此处用is_authenticated是因为返回的是Json对象,而不是Response对象
        if not request.user.is_authenticated():
            # 用户未登录,返回错误信息到Ajax,Ajax再根据code的值进行判断
            return JsonResponse({"code": 1, "errmsg": "用户未登录"})
        # 获取参数 订单order_id
        # 通过request中的GET属性,通过字典的get函数获取健名为订单号order_id的值,获取不到为None
        order_id = request.GET.get('order_id')
        # 校验参数,如果没有获取到值,直接返回
        if not order_id:
            # 返回错误信息到Ajax,Ajax再根据code的值进行判断
            return JsonResponse({"code": 2, "errmsg": "参数有误"})
        # 根据request对象获取用户
        user = request.user
        # 查询数据库,判断订单号是否存在
        try:
            # 查询到会返回对象,没有会与异常
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          status=OrderInfo.ORDER_STATUS_ENUM["UNPAID"],
                                          pay_method=OrderInfo.PAY_METHODS_ENUM['ALIPAY'])
        # 抛出没有找到的异常
        except OrderInfo.DoesNotExist:
            # 返回错误信息到Ajax,Ajax再根据code的值进行判断
            return JsonResponse({"code": 3, "errmsg": "订单信息有误"})
        # 向支付宝查询支付结果
        # 创建支付宝支付工具的对象
        alipay_client = AliPay(
            appid=settings.ALIPAY_APPID,
            # 支付完成跳转回的连接地址
            app_notify_url=None,
            # 用户的自己的私钥,公钥在支付宝端已经配置好
            app_private_key_path=os.path.join(settings.BASE_DIR,"apps/orders/keys/app_private_key.pem"),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(settings.BASE_DIR,"apps/orders/keys/alipay_public_key.pem"),
            # 加密方式 RSA 或者 RSA2
            sign_type="RSA2",
            # 沙箱环境,默认False,
            debug=True,
        )
        # 向支付宝查询支付结果
        while True:
            # 通过alipay客户端调用api_alipay_trade_query函数查询支付结果,返回的是对象
            # out_trade_no为用户订单号
            result = alipay_client.api_alipay_trade_query(out_trade_no=order_id)
            # 支付宝返回的接口调用结果,code="10000" 表示支付宝处理正确,其他表示支付宝异常
            alipay_result_code = result.get("code")
            # code="40004" 表示支付宝那边支付信息还没有生成，可以稍后再查询，获取结果
            # 即系统发起请求时,支付宝还没有建立起支付链接,需等待后查询
            if alipay_result_code != "10000" and alipay_result_code != "40004":
                # 表示支付宝异常,直接返回结果到Ajax
                return JsonResponse({"code": 1, "errmsg": "支付宝异常"})
            # 当code = 40004的时候,表示支付链接没有建立
            elif alipay_result_code == "40004":
                # 延时5秒,再去请求
                time.sleep(5)
                # 继续下一次查询
                continue
            # 表示code=10000,支付宝调用成功,查询返回的状态信息
            trade_status = result.get("trade_status")
            # 此处WAIT_BUYER_PAY表示在等待买家付款,需稍后查询
            if trade_status == "WAIT_BUYER_PAY":
                # 延时5秒
                time.sleep(5)
                # 继续下一次查询
                continue
            # TRADE_SUCCESS表示支付成功或者TRADE_FINISHED表示支付完成
            # 即此处表示用户已经支付完成了
            elif trade_status == "TRADE_SUCCESS" or trade_status == "TRADE_FINISHED":
                # 得到支付结果信息后，保存数据库数据
                # 获取第三方的支付的支付交易号
                trade_no = result.get("trade_no")
                # 修改订单表的数据状态
                # 将支付状态改为待评价,此处应该是待发货
                order.status = OrderInfo.ORDER_STATUS_ENUM["UNCOMMENT"]
                # 获取订单号
                order.order_id = trade_no
                # 保存到数据库中
                order.save()
                # 返回Json对象会Ajax,告知成功,状态码0,其中errmsg在工作中要写英文
                return JsonResponse({"code": 0, "errmsg": "支付成功"})
            # 其他情况
            else:
                # 说支付不成功,返回到Ajax页面,告知页面处理
                return JsonResponse({"code": 2, "errmsg": "用户支付未成"})

