from django.conf.urls import url


from . import views

urlpatterns = [
    # 方法1.使用视图函数调用对应的请求
    # url(r'^register$', views.register, name="register")
    # 方法2.使用类的模式定义视图函数,通过不同的请求调用不同的类方法
    # 使用as_view方法，将类视图转换为函数
    url(r'^register$', views.RegisterView.as_view(), name="register"),
    # 激活请求的路由,定义类同上
    url(r'^active/(?P<user_token>.+)$', views.UserActiveView.as_view(), name="active"),
    # 用户登陆的请求
    url(r'^login$', views.LoginView.as_view(), name="login"),

]