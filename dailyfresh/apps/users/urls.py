"""定义用户管理相关的url请求"""
# django核心模块,用于定义用户请求的url
from django.conf.urls import url
# 从当前路径下导入视图模块 .代表当前模块
from . import views
# login_required为django系统中用于控制用户访问权限的装饰器,一般不在url中使用
# 通常是在 utils 模块中自定义组件来管理用于访问权限
# from django.contrib.auth.decorators import login_required


urlpatterns = [
    # 方法1.使用视图函数调用对应的请求
    # url(r'^register$', views.register, name="register")
    # 方法2.使用类的模式定义视图函数,通过不同的请求调用不同的类方法
    # 使用as_view方法，根据不同的请求方式get或post将类视图转换为视图函数
    # 即get方式时:views.RegisterView.as_view()的结果为views.get
    # post方式时:views.RegisterView.as_view()的结果为views.post
    url(r'^register$', views.RegisterView.as_view(), name="register"),
    # 激活请求的路由,定义类同上
    url(r'^active/(?P<user_token>.+)$', views.UserActiveView.as_view(), name="active"),
    # 用户登陆
    url(r'^login$', views.LoginView.as_view(), name="login"),
    # 退出
    url(r'^logout$', views.LogoutView.as_view(), name="logout"),
    # 第一种验证用户是否登陆的装饰器使用方法
    # url(r'^address$', login_required(views.AddressView.as_view()), name="address"),
    # 用户地址
    url(r'^address$', views.AddressView.as_view(), name="address"),
    # 用户信息
    url(r'^info$', views.UsersInfoView.as_view(), name="info"),
    # 用户购物车
    url(r'^cart$', views.UsersCartView.as_view(), name="cart"),
    # 用户订单
    url(r'^order$', views.UsersOrderView.as_view(), name="order"),

]