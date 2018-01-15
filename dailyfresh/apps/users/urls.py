from django.conf.urls import url


from . import views

urlpatterns = [
    # url(r'^register$', views.register, name="register")
    # 使用as_view方法，将类视图转换为函数
    url(r'^register$', views.RegisterView.as_view(), name="register")
]