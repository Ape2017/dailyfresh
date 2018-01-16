import re
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from users.models import User
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from utils import constants
from django.conf import settings
from celery_task.tasks import send_active_email


# 函数视图(原始)
# def register(request):
#     """注册模块"""
#     if request.method == "GET":
#         return render(request, "register.html")
#     else:
#         # post
#         # 接收表单数据，
#         pass
# 视图类(工程用)
class RegisterView(View):
    """注册类视图"""

    def get(self, request):
        """对应get请求方式的逻辑"""
        return render(request, "register.html")

    def post(self, request):
        """
        对应post请求方式的业务逻辑处理
        :param (参数0) request: 用户请求数据
        :return(返回值2): 返回response数据
        """
        # 1.1.获取用户输入的数据: 用户名,密码,确认密码,邮箱,是否同意协议
        user_name = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 1.2.参数校验
        # python中0 0.0 空字符串'' 空列表[] 空元祖() 空字典{} 空None False 均为假
        # all处理所有的元素,只有所有元素都为真,all函数才会返回真,否则返回假
        if not all([user_name, password, password2, email, allow]):
            # 参数不完整
            # reverse 逆向解析
            url = reverse('users:register')
            # redirect()参数:url 重定向:返回的是一个请求链接
            return redirect(url)
        # 判断两次密码是否一致
        if password != password2:
            return render(request, 'register.html', {'errmsg': '两次密码不一致'})
        # 判断邮箱格式是否正确
        # re.search()不严格匹配
        # re.match() 严格匹配
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            # 邮箱不匹配
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 判断是否勾选了协议
        # 复习:前端事件
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意服务协议'})

        # 1.3.业务处理
        # 1.3.1判断用户名是否存在
        try:
            # 保存数据到数据库中
            # create_user方法是django用户认证系统提供的
            # 会帮助我们加密密码并保存到数据库中
            user = User.objects.create_user(user_name, email, password)
        except IntegrityError as e:
            # 表示用户名已注册
            return render(request, 'register.html', {'errmsg': '用户名已经注册'})
        # 1.3.2更改用户的激活状态,将默认的已激活状态改为未激活状态
        user.is_active = False
        user.save()

        # 1.3.3生成用户激活的身份 token(令牌)
        # 模型类中定义了generate_active_token方法,返回值为token的字符串
        token = user.generate_active_token()

        # 1.3.4拼接激活的连接
        active_url = 'http://127.0.0.1:8000/users/active/%s' % token

        # 1.3.5发送邮件
        # 1.3.5.1同步发送邮件(阻塞模式,效率不高)
        # 发送激活的邮件
        # send_mail(邮件标题,邮件内容,发件人,收件人,html_message=html格式的邮件内容)
        # html_message = """
        # <h1>天天生鲜用户激活</h>
        # <p>%s<p>
        # <a href=%s>%s</a>
        # """%(user_name, active_url, active_url)
        # send_mail('天天生鲜','',settings.EMAIL_FROM,[email],html_message=html_message)

        # 1.3.5.2异步发送邮件(非阻塞)
        send_active_email.delay(user_name, active_url, email)

        # 2.返回值
        return HttpResponse('注册成功')


class UserActiveView(View):
    """用户激活视图"""

    def get(self, request, user_token):
        """
        用户激活
        :param request:
        :param user_token: 用户激活令牌
        :return:
        """
        # 创建转换工具对象 (序列化)
        s = Serializer(settings.SECRET_KEY, constants.USER_ACTIVE_EXPIRES)
        try:
            data = s.loads(user_token)
        except SignatureExpired:
            return HttpResponse('链接已过期')
        # 获取用户名
        user_id = data.get('user_id')

        # 更新用户的激活状态
        try:
            # User.objects.filter(id=user_id).update(is_active=True)
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # 如果不存在,会抛出这个异常
            return HttpResponse('用户不存在')

        user.is_active = True
        user.save()

        return render(request, "login.html")
