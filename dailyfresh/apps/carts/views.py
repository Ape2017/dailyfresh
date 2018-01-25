"""
购物车app的视图模块,主要处理用户对购物车的增,删,改,查
"""
# render返回模板文件
from django.shortcuts import render
# View系统默认类视图
from django.views.generic import View
# 返回到前端的Json数据,接受字典,返回Json
from django.http import JsonResponse
# 商品表的goods_sku表
from goods.models import GoodsSKU
# 获取redis对象的方法
from django_redis import get_redis_connection
# 导入json ,使用dumps和loads函数
import json
# 常量模块,使用CART_INFO_COOKIE_EXPIRES的时间
from utils import constants
# Decimal 数据类型模块,类似float类型
from decimal import Decimal


# 显示购物车信息,查询cookies和redis
class InfoView(View):
    """购物车数据信息"""
    print("infoinfoinfo")
    def get(self, request):
        """提供购物车页面"""
        # 获取购物车的数据
        # 用户未登录,从cookie读取
        if not request.user.is_authenticated():
            cart_json_str = request.COOKIES.get('cart_info')
            if cart_json_str:
                # 表示有购物车数据
                cart_dict = json.loads(cart_json_str)
            else:
                # 购物车中没数据,设置成空字典
                cart_dict = {}
        # 用户已登录,从redis中读取
        else:
            user = request.user
            redis_conn = get_redis_connection('default')
            # 此处cart_dict里的数据(键和值)是字节类型
            cart_dict = redis_conn.hgetall('cart_%s' % user.id)
            # print(cart_dict)
            # {b'1': b'5', b'5': b'6', b'7': b'3'}
            # 如果登录用户的购物车没有数据
            if cart_dict is None:
                # 设置成空字典
                cart_dict = {}

        # {"id":"", "id":""...}
        # GoodsSKU.objects.filter(id__in=cart_dict.keys())
        # 初始化存储数据的变量,用于下面使用
        # skus代表sku对象的列表,也就是存储在购物车中的商品对象
        skus_list = []
        # 购物车中的商品的总金额
        total_amount = 0
        # 购物车中的商品的总数量
        total_count = 0
        # 遍历购物车中的数据,获取sku_id(商品id)和sku_count(数量)
        for sku_id, sku_count in cart_dict.items():
            # 根据sku_id获取商品的sku对象
            # 此处若是从COOKIES中拿到的数据,sku_id是字符串型数据
            # 此处若是从redis中拿到的数据,sku_id是字节型数据
            # print(sku_id)
            sku = GoodsSKU.objects.get(id=sku_id)
            # 此处若是从COOKIES中拿到的数据,sku_count是字符串型数据
            # 此处若是从redis中拿到的数据,sku_count是字节型数据
            # 将字符类型转换成int类型
            sku_count = int(sku_count)
            # 将int类型转换成Decimal类型
            sku_count = Decimal(sku_count)
            # 商品总金额,添加到sku对象的属性中
            sku.amount = sku.price * sku_count
            # 商品数量
            sku.count = sku_count
            # 将sku对象添加到skus列表中中
            skus_list.append(sku)
            # 购物车总商品金额
            total_amount += sku.amount
            # 购物车总商品数量
            total_count += sku.count
        # 生产上下文对象
        context = {
            'skus': skus_list,
            'total_amount': total_amount,
            'total_count': total_count,
        }
        # 返回指定页面
        return render(request, 'cart.html', context)


# 用户添加商品到购物车中
class AddView(View):
    """
    通过Ajax进行请求
    添加商品到购物车,
    登录时购物车信息存储到redis中
    未登录时存储到COOKIES中
    method:POST
    url:carts/add
    请求数据:数据放到请求体中(仿照表单格式)
    """
    print('ADDADDADD')
    def post(self, request):
        """
        处理用户在前端的操作,通过Ajax请求
        :param request: 请求对象
        :return: 返回提示信息
        """
        # 获取参数 sku_id sku_coount
        # 保存在POST中,通过get方法获取
        sku_id = request.POST.get('sku_id')
        sku_count = request.POST.get('sku_count')
        # 校验参数
        if not all([sku_id, sku_count]):
            # 返回JSON数据,实际开发中errmsg返回的数据要返回英文,
            return JsonResponse({"code": 1, "errmsg": '参数不完整'})
        # 判断添加商品的数量类型是否正确
        try:
            sku_count = int(sku_count)
        except Exception:
            # 返回提示信息
            return JsonResponse({"code": 2, "errmsg": '商品数量参数有误'})
        # 判断商品是否存在
        try:
            # 根据sku_id获取当前商品的对象
            # 此处sku_id为字符串类型
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 如果获取失败,表示商品不存在
            return JsonResponse({"code": 3, "errmsg": '商品不存在'})

        # 判断库存
        if sku_count > sku.stock:
            # 如果添加的数量超过库存,返回提示信息
            return JsonResponse({"code": 4, "errmsg": '库存不足'})

        # 业务处理
        # 判断用户的登录状态,用户登录情况下增加到redis中
        if request.user.is_authenticated():
            # 获取用户对象
            user = request.user
            # 获取default的redis对象
            redis_conn = get_redis_connection('default')
            # 先获取原有购物车中的这个商品的数量,如果没有数据,返回None
            # hget是哈希函数,参考http://redisdoc.com/index.html
            # hget(self, name, key) 方法是通过redis存储健名和keys的健名,获取到值
            origin_count = redis_conn.hget("cart_%s" % user.id, sku_id)
            # 判断origin_count数据的有效性
            if origin_count:
                # 如果购物车中有原先的记录,商品数量累加
                sku_count += int(origin_count)

            # 将用户新增的一条数据保存到数据库中
            # 此处的sku_count如果没有累加,为用户传过来的数据(112行处)
            # 如果累加,为累加后的数据
            # hset(self,name,key,value)将hash数据保存到redis中
            # hset中name代表存储的健名,其中值为hash类型,hash的键为key,hash的值的值为value
            # 存储结构类似{user_id : {sku_id: sku_count}}
            redis_conn.hset('cart_%s' % user.id, sku_id, sku_count )

            # 获取此用户购物车中所有的商品id和数量,为一个字典,键为商品id,值为用户添加该商品的数量
            cart_dict = redis_conn.hgetall('cart_%s' % user.id)
            # 定义cart_num并且初始化为0
            cart_num = 0
            # 遍历字典的values值,通过values函数
            for val in cart_dict.values():
                # 累加数量,获取总数
                cart_num += int(val)
            # 返回数据
            # Json数据里面必须时双引号
            # '{"code": 0, "errmsg": "添加成功"}'  json
            return JsonResponse({"code": 0, "errmsg": '添加成功',"cart_num": cart_num})
        else:
            # 用户未登录,保存到cookie中,cookie为序列化后的字符串
            # 先从cookie中尝试获取用户的购物车数据
            # '{sku_id:sku_count,.....}'
            cart_json_str = request.COOKIES.get('cart_info')
            # 判断cookie中是否存有值
            if cart_json_str:
                # 将json字符串转换为字典
                cart_dict = json.loads(cart_json_str)
            else:
                cart_dict = {}
            # 获取购物车原有商品的数量
            origin_count = cart_dict.get(sku_id)
            # 数量累计
            if origin_count:
                sku_count += origin_count
            # 将商品的新数量保存到购物车字典数据中
            cart_dict[sku_id] = sku_count

            # 求取购物车商品的总数量
            cart_num = 0
            # 遍历字典中的values中,获取购物车中商品总数
            for val in cart_dict.values():
                # cart_num 购物车总数量
                cart_num += val

            # 将购物车数据转换为json字符串，用于保存到cookie中
            new_cart_json_str = json.dumps(cart_dict)

            # 将购物车数据设置在cookie中
            resp = JsonResponse({"code": 0, "errmsg": '添加成功', "cart_num": cart_num})

            # 设置cookie
            resp.set_cookie('cart_info', new_cart_json_str, max_age=constants.CART_INFO_COOKIE_EXPIRES)

            # 返回数据
            return resp


# 更新购物车数据
class UpdateView(View):
    """
    购物车商品数量更新
    前端还是Ajax请求模式
    此处采用幂等请求,请求数据是最终存在数据库中的数据
    """
    print('UPPUPPUPP')
    def post(self,request):
        """
        用于用户操作购物车页面时,对商品数量的增加和减少
        Ajax请求模式
        :param request:请求对象
        :return: Json数据
        """
        # 获取参数
        # 商品ID
        sku_id = request.POST.get('sku_id')
        # 商品数量
        sku_count = request.POST.get('sku_count')
        print(sku_id)
        print(sku_count)
        # 校验参数
        if not all([sku_id,sku_count]):
            # 参数不完整,返回提示
            return JsonResponse({'code':1,'errmsg':'参数不完整'})
        # 商品是否存在
        try:
            # 获取商品的对象
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 出现异常,返回提示
            return JsonResponse({'code':2,'errmsg':'商品信息有误'})
        # 数量是否正确
        try:
            # 此处sku_count为字符串类型,转换成整形
            sku_count = int(sku_count)
        except Exception:
            # 出现异常,返回提示
            return JsonResponse({'code':3,'errmsg':'数量信息有误'})
        # 判断传过来的数量是否超过库存
        if sku.stock < sku_count:
            return JsonResponse({'code': 4, 'errmsg': '库存不足'})
        # 保存数据,判断用户登录情况
        # 如果用户未登录
        if not request.user.is_authenticated():
            # 用户为登录的情况,更新COOKIE
            # 获取用户COOKIES中存取的信息
            cart_json_str = request.COOKIES.get('cart_info')
            # 如果有数据
            if cart_json_str:
                # 将Json用loads函数转换成字典
                cart_dict = json.loads(cart_json_str)
            # 如果没有数据
            else:
                # 将cart_dict设置空字典
                cart_dict = {}
            # 设置商品的数量到字典中
            # 因为此链接为幂等,数据是最终存储的,不用查询之前的数据进行累加
            # 此处sku_id为字符串
            cart_dict[sku_id] = sku_count
            # 设置视图返回对象
            resp = JsonResponse({'code':0,'errmsg': '设置成功'})
            # 通过返回对象设置COOKIE
            # set_cookie(name,Json,max_age)分别代表cookie名字,Json数据字符串,max_age有效期
            resp.set_cookie('cart_info', json.dumps(cart_dict),max_age=constants.CART_INFO_COOKIE_EXPIRES)
            # 返回设置了cookie的对象
            return resp
        # 如果用户已登录
        else:
            # 获取登录的用户对象
            user = request.user
            # 获取redis用户对象,用来操作购物车数据
            redis_conn = get_redis_connection('default')
            # 将数据存储到redis购物车中
            # 因为是幂等的,不计算累加信息(幂等为最终数据)
            # hset(self,name,key,value)以hash数据保存到redis中
            # hset中name代表存储的健名,其中值为hash类型,hash的键为key,hash的值的值为value
            # 存储结构类似{user_id : {sku_id: sku_count}}
            redis_conn.hset('cart_%s' % user.id, sku_id, sku_count)
            # 返回提示信息
            return JsonResponse({'code': 0,'errmsg': '设置成功'})


# 用户删除购物车记录
class DeleteView(View):
    """
    用户通过Ajax进行删除购物车数据的请求,收到请求后,
    通过查询cookie和redis,删除对应的商品信息
    """
    print('DELDELDEL')
    def post(self,request):
        """
        删除购物车数据
        请求来自Ajax
        :param request:用户请求
        :return: Json提示信息
        """
        # 获取参数
        # 需要删除的sku_id
        sku_id = request.POST.get('sku_id')
        print(sku_id)
        # 若获取不到sku_id,说明参数不正确
        if not sku_id:
            # 返回提示信息
            return JsonResponse({'code': 1,'errmsg':'参数不完整'})
        # 删除购物车数据
        # 判断用户登录情况
        # 用户未登录,删除cookie中的数据
        if not request.user.is_authenticated():
            # 获取购物车的Json字符串
            cart_json_srt = request.COOKIES.get('cart_info')
            # 判断是否获取成功
            # 如果有数据
            if cart_json_srt:
                # 将Json字符串转换成字典
                cart_dict = json.loads(cart_json_srt)
            # 如果没有数据
            else:
                # 将cart_dict设置成空字典
                cart_dict = {}
            # 判断商品id是否在字典中,此处sku_id为上面获取的参数
            # 也就是说用户要删除商品在不在cookie中存储这
            # 如果不在,可以忽略
            if sku_id in cart_dict:
                # 在,删除对应的键值对
                del cart_dict[sku_id]
            # 设置返回对象,并将提示信息加载到对象中
            resp = JsonResponse({'code': 0, 'errmsg': '删除成功'})
            # 重新设置删除后返回对象的cookie,用于设置在前端浏览器中
            # set_cookie(name,Json,max_age)分别代表cookie名字,Json数据字符串,max_age有效期
            resp.set_cookie('cart_info', json.dumps(cart_dict), max_age=constants.CART_INFO_COOKIE_EXPIRES)
            # 返回返回对象
            return resp
        # 如果用户是已登录状态
        else:
            # 获取用户对象
            user = request.user
            # 获取操作购物车的redis对象
            redis_conn = get_redis_connection('default')
            # 用redis对象操作对应的数据
            # 删除哈希表 key 中的一个或多个指定域，不存在的域将被忽略。
            # 此处返回的是删除数据的条数,如果没有将返回0
            redis_conn.hdel('cart_%s' % user.id, sku_id)
            # 返回处理后的Json对象和提示信息
            return JsonResponse({'code': 0, 'errmsg': '删除成功'})
