# 正则匹配模块 校验邮箱时使用
import re
# 返回http页面
from django.http import HttpResponse
# ***反向解析***
from django.core.urlresolvers import reverse
# 返回render(渲染页面)和redirect(重定向)路径
from django.shortcuts import render, redirect
# 视图类处理用户请求,比视图函数强
from django.views.generic import View
# 用户模型类,地址
from users.models import User, Address
# django数据库包异常信息,数据重复,字段内设置了唯一
from django.db import IntegrityError
# Django发送邮件包
from django.core.mail import send_mail
# 生成签名(序列化)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
# 常量模块
from utils import constants
# 系统配置
from django.conf import settings
# 通过委托发送邮件 celery(分布式任务队列)
from celery_task.tasks import send_active_email
# 系统自带用户认证组件,认证(校验用户名和密码),登录,退出,
from django.contrib.auth import authenticate, login, logout
# 系统校验用户是否是登陆状态
from django.contrib.auth.decorators import login_required
# 自定义组件,进行访问权限校验,若是已登陆,访问请求页面,若未登陆,重定向到登陆页面
from utils.commons import LoginRequiredMixin


# 用户注册
class RegisterView(View):
    """注册类视图,继承View类注册业务逻辑"""

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
            return render(request, 'register.html', {'errmsg': '密码不一致,请重新输入'})
        # 判断邮箱格式是否正确
        # re.search()不严格匹配
        # re.match() 严格匹配
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            # 邮箱不匹配
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确,请重新输入'})
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
            return render(request, 'register.html', {'errmsg': '用户名已注册,请重新输入'})
        # 1.3.2更改用户的激活状态,将默认的已激活状态改为未激活状态
        user.is_active = False
        user.save()

        # 1.3.3生成用户激活的身份 token(令牌)
        # 模型类中定义了generate_active_token方法,返回值为token的字符串
        token = user.generate_active_token()

        # 1.3.4拼接激活的链接
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
        # 通过任务执行调用任务的快捷方式delay函数执行添加队列
        send_active_email.delay(user_name, active_url, email)

        # 2.返回注册成功信息,提示激活
        url = reverse('users:login')
        # print('重定向路由:'+ url)
        # redirect()参数:url 重定向:返回的是一个请求链接
        return redirect(url)


# 账户激活
class UserActiveView(View):
    """用户激活视图"""

    def get(self, request, user_token):
        """
        用户激活
        :param request:
        :param user_token: 用户激活令牌
        :return:
        """
        # 创建转换工具对象 (字串序列化)
        s = Serializer(settings.SECRET_KEY, constants.USER_ACTIVE_EXPIRES)
        try:
            data = s.loads(user_token)
        except SignatureExpired:
            return HttpResponse('链接已过期')
        # 获取用户名
        # 此次data为字典,使用get取值而不用key取值是因为get取值异常时返回None,而key取值则会报keyerror错误
        user_id = data.get('user_id')

        # 更新用户的激活状态
        try:
            # User.objects.filter(id=user_id).update(is_active=True)
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # 如果不存在,会抛出这个异常
            return HttpResponse('用户不存在')
        # 将用户激活字段更改为已激活
        user.is_active = True
        # 保存
        user.save()
        # 逆向解析登陆的url,返回到登陆页面
        url = reverse('users:login')
        # redirect()参数:url 重定向:返回的是一个请求链接
        return redirect(url)


# 用户登陆
class LoginView(View):
    """登陆模块业务逻辑"""
    # get方式请求的url有:
    # 1./users/login?next=/users/address
    # 2./users/login
    # requestGET模式:从查询字符串中获取参数
    # requestPOST模式:从请求体中获取参数
    def get(self, request):
        """对应get请求方式的逻辑"""
        return render(request, "login.html")

    def post(self, request):
        """
        对应post请求方式的业务逻辑处理
        :param (参数0) request: 用户请求数据
        :return(返回值2): 返回response数据
        """
        # 1.1.获取用户输入的数据: 用户名,密码
        # POST从请求体获取数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 1.2.参数校验
        # python中0 0.0 空字符串'' 空列表[] 空元祖() 空字典{} 空None False 均为假
        # all处理所有的元素,只有所有元素都为真,all函数才会返回真,否则返回假
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '用户名密码不能为空'})
        # 1.3 业务处理
        # 原始思路
        # 判断用户名或密码是否正确
        # 判断用户名或密码是否正确
        # 根据用户名查询数据库,获取用户的密码信息
        # user = User.objects.get(username=user_name)
        # 对用户输入的登陆密码惊喜加密处理,然后于数据库查询的密码惊喜对比,如果相同,表示登陆成功,否则失败
        # user_password = sha256(password)
        # if password ==  user_password

        # 使用django自带的认证系统
        user = authenticate(username=username, password=password)
        if user is None:
            # 认证失败
            return render(request, 'login.html', {'errmsg': '用户名密码错误'})
        # 表示用户名密码正确
        # 判断判断激活状态
        if user.is_active is False:
            # 表示用户未激活
            return render(request, 'login.html', {'errmsg': '账户未激活'})

        # 登陆成功
        # 记录用户的登陆状态到session中
        # 使用Django的认证系统记录用户登陆
        login(request, user)

        # 判断用户是否勾选记录用户名()
        remember = request.POST.get('remember')
        if remember == 'on':
            # 表示用户勾选了用户名
            # None表示Django默认的有效期 两周
            # 传入秒数 表示失效期
            request.session.set_expiry(None)
        else:
            # 关闭浏览器就失效
            request.session.set_expiry(0)

        # 从查询字符串中尝试获取next的参数
        # GET 从查询字符串中获取参数
        next_url = request.GET.get('next')
        if next_url is None:
            next_url = reverse('goods:index')
        # 返回,引导用户跳转到next指定的页面
        return redirect(next_url)


# 用户退出
class LogoutView(View):
    """用户退出视图"""

    def get(self, request):
        """退出"""
        # 清除用户的登陆数据 session
        # 使用django自带认证系统的退出
        logout(request)
        # 退出后,引导用户到登陆页面
        return redirect(reverse('users:login'))


# 用户个人中心:收货地址
class AddressView(LoginRequiredMixin, View):
    """用户地址"""
    def get(self, request):
        """提供地址页面数据"""
        # 判断用户的登陆状态
        # 如果用户未登陆,则跳转到登陆页面
        # 如果已经登陆,显示地址信息
        # 通过系统处理登陆状态
        # 查询数据库,获取用户的地址信息
        # 显示在页面上
        user = request.user
        # 取出数据库中最后更新一条数据
        # 方式一
        # Address.objects.filter(user=user).order_by('-update_time')[0]
        # 方式二
        # django取第一条
        # user.address_set.order_by('-update_time')[0]
        try:
            # latest方法 取最新一条
            address = user.address_set.latest('update_time')
        except Address.DoesNotExist:
            # 表示数据库中没有这个用户地址数据
            address = None
        # 将地址信息返回到模板页面中
        return render(request, 'user_center_site.html', {'address': address})

    def post(self, request):
        """保存用户地址数据"""
        # 获取当前登陆的用户对象
        user = request.user
        # 用于显示当前地址
        try:
            # latest方法 取最新一条
            address = user.address_set.latest('update_time')
        except Address.DoesNotExist:
            # 表示数据库中没有这个用户地址数据
            address = None
        # 获取request对象中body的收件人名字
        receiver_name = request.POST.get('receiver_name')
        # 新建收件人地址
        new_detail_address = request.POST.get('address')
        # 邮编
        zip_code = request.POST.get('zip_code')
        # 手机
        mobile = request.POST.get('mobile')
        # 判断全部输入中是否有空
        if not all([receiver_name, new_detail_address, zip_code, mobile]):
            return render(request, "user_center_site.html",{"address": address, "errmsg": "数据不完整"})
        # 保存数据到数据库中
        # 方式一:
        # new_address = Address(
        #     user=user,
        #     receiver_name=receiver_name,
        #     receiver_mobile=mobile,
        #     detail_addr=new_detail_address,
        #     zip_code=zip_code)
        # new_address.save()
        # 方式二:
        # new_address = Address()
        # new_address.user = user
        # new_address.receiver_name = receiver_name
        # new_address.receiver_mobile = mobile
        # new_address.detail_addr = new_detail_address
        # new_address.zip_code = zip_code
        # 方式三:
        Address.objects.create(
            user=user,
            receiver_name=receiver_name,
            receiver_mobile=mobile,
            detail_addr=new_detail_address,
            zip_code=zip_code
        )
        return redirect(reverse('users:address'))


class InfoView(LoginRequiredMixin, View):
    """用户地址"""

    def get(self, request):
        """提供地址页面数据"""
        # 判断用户的登陆状态
        # 如果用户未登陆,则跳转到登陆页面
        # 如果已经登陆,显示地址信息
        # 通过系统处理登陆状态
        # 查询数据库,获取用户的地址信息
        # 显示在页面上
        user = request.user
        # 取出数据库中最后更新一条数据
        # 方式一
        # Address.objects.filter(user=user).order_by('-update_time')[0]
        # 方式二
        # django取第一条
        # user.address_set.order_by('-update_time')[0]
        # try:
        #     # latest方法 取最新一条
        #     address = user.address_set.latest('update_time')
        # except Address.DoesNotExist:
            # 表示数据库中没有这个用户地址数据
            # address = None
        # 将地址信息返回到模板页面中
        return render(request, 'user_center_info.html')


class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'user_center_order.html')