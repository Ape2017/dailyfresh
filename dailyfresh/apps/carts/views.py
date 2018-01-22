from django.shortcuts import render  # render返回模板文件
# View系统默认类视图
from django.views.generic import View
# 自定义组件,限制用户访问权限,登陆状态:允许访问 未登陆状态:跳转到主页
from utils.commons import LoginRequiredMixin
# 获取redis对象的方法
from django_redis import get_redis_connection
# 商品表的goods模块
from goods.models import GoodsSKU
# 返回到前端的Json数据,接受字典,返回Json
from django.http import JsonResponse
# 导入json ,使用dumps和loads
import json
# 常亮模块
from utils import constants


# 用户添加商品到购物车中
class AddView(View):
    """
    添加商品到购物车,购物车信息存储到redis中
    method:POST
    url:carts/add
    请求数据:数据放到请求体中(仿照表单格式)
    """
    def post(self, request):
        # 获取参数 sku_id sku_coount
        sku_id = request.POST.get('sku_id')
        sku_count = request.POST.get('sku_count')
        # 校验参数
        if not all([sku_id, sku_count]):
            # 公司中要返回英文
            return JsonResponse({"code": 1, "errmsg": '参数不完整'})
        # 判断商品数量类型是否正确
        try:
            sku_count = int(sku_count)
        except Exception:
            return JsonResponse({"code": 2, "errmsg": '商品数量参数有误'})

        # 判断商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"code": 3, "errmsg": '商品不存在'})

        # 判断库存
        if sku_count > sku.stock:
            return JsonResponse({"code": 4, "errmsg": '库存不足'})
        # 业务处理
        # 判断用户的登录状态,用户登录情况下的购物车添加(添加一个商品)
        if request.user.is_authenticated():
            # 获取用户
            user = request.user
            # 获取default的redis对象
            redis_conn = get_redis_connection('default')
            # 先获取原有购物车中的这个商品的数量,如果没有数据,返回None
            origin_count = redis_conn.hget("cart_%s" % user.id, sku_id)
            # 判断数据情况
            if origin_count:
                # 如果购物车中有原先的记录,数量累加
                sku_count += int(origin_count)

            # 将用户新增的一条数据保存到数据库中
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
            for val in cart_dict.values():
                cart_num += val

            # 将购物车数据转换为json字符串，用于保存到cookie中
            new_cart_json_str = json.dumps(cart_dict)

            # 将购物车数据设置在cookie中
            resp = JsonResponse({"code": 0, "errmsg": '添加成功', "cart_num": cart_num})

            # 设置cookie
            resp.set_cookie('cart_info', new_cart_json_str, max_age=constants.CART_INFO_COOKIE_EXPIRES)

            # 返回数据
            return resp







