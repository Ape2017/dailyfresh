# 系统自带的用户访问权限管理模块,login_required 登录状态装饰器
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse


# def login_required_json(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated():
#             return JsonResponse({'code': 1, 'message': '用户未登录'})
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper

class LoginRequiredMixin(object):
    """自定义组件模块,用于校验用户访问权限等功能"""

    @classmethod
    def as_view(cls, *args, **kwargs):
        """
        目的:该类方法是通过Django系统中的装饰器login_required装饰Django的视图类View中的as_view方法.达到控制用户访问权限的目的
        逻辑:
            1.通过类的多继承方式,使需要验证用户访问权限的视图类先继承该组件,再继承Django的视图类View
            2.重写as_view方法,因为视图函数是以类方法实现,可以用classmethod装饰器使as_view方法变成类方法
            3.由于自定义的类视图是多继承该组件和视图类View的,MRO顺序表 cls--->LoginRequiredMixin--->View
            4.通过super函数调用View类视图中的as_view方法并返回一个view函数
            5.super(A,cls).as_view():表示在类对象cls和类A有继承关系时,通过super函数调用的方法是类cls的MRO顺序中A的上一级的类中的方法
            6.通过装饰器login_required装饰super函数返回的view函数,当用户未登陆时会重定向到指定的url(settings.LOGIN_URL)页面
            7.返回装饰后的view函数,供系统使用
        :param args:
        :param kwargs:
        :return: 装饰后的view函数
        """
        view = super(LoginRequiredMixin, cls).as_view(*args, **kwargs)
        view = login_required(view)
        return view


class TransactionAtomicMixin(object):
    """事务支持扩充"""
    @classmethod
    def as_view(cls, *args,**kwargs):
        view = super(TransactionAtomicMixin, cls) .as_view(*args, **kwargs)
        view = transaction.atomic(view)
        return view
