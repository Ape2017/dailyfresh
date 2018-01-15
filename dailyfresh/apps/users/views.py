from django.shortcuts import render
from django.views.generic import View

# Create your views here.


# def register(request):
#     """注册"""
#     if request.method == "GET":
#         return render(request, "register.html")
#     else:
#         # post
#         # 接收表单数据，
#         pass


# 类视图
class RegisterView(View):
    """注册类视图"""
    def get(self, request):
        """对应get请求方式的逻辑"""
        return render(request, "register.html")

    def post(self, request):
        """对应post请求方式的逻辑"""
        pass
