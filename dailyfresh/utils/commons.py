"""自定义组件模块,用于校验用户访问权限等功能"""
# 系统自带的用户访问权限管理模块,login_required 登录状态装饰器
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    """
        功能:用户访问权限的装饰类,是定义的类视图扩展类，作用是向类视图中补充验证用户登录的逻辑
        逻辑:
            1.通过类继承机制,使视图类继承此扩展类和系统的视图类View.
            2.重写as_view方法,通过super()函数通过视图对象调用视图类中的as_view方法,并返回一个view函数
            3.通过装饰器login_required装饰view函数
            4.as_view方法返回一个view函数.
    """

    @classmethod
    def as_view(cls, *args, **kwargs):
        # super寻找调用类的下一个父类的as_view()
        # MRO顺序表 cls--->LoginRequiredMixin--->View
        # super()函数参数1:自身类对象 参数2:调用本方法的类对象
        # super(LoginRequiredMixin,cls) 首先找到 LoginRequiredMixin 的MRO上一级的类（就是类View）
        # 然后把传入的类对象cls转换为类View的对象
        view = super(LoginRequiredMixin, cls).as_view(*args, **kwargs)
        # 使用django认证系统提供的装饰器
        # 如果用户未登陆,会将用户引导到settings.LOGIN_URL指明的登陆页面
        view = login_required(view)

        return view
