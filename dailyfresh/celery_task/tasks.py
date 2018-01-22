# 受django委托发送邮件方 celery(分布式任务队列)
from celery import Celery
# 将django项目的配置文件信息保存到操作系统中
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dailyfresh.settings'
# 在启动celery的时候需要，在启动django的时候不需要，需要注释掉
# 让django初始化一下，django读入配置文件的信息
# django.setup()会询问操作系统配置文件的位置，读入配置文件的信息
# 以下两行在启动celery时打开注释,启动Django时注释
# import django
# django.setup()
# 启动celery的命令
# celery -A celery_task.tasks worker -l info
# django系统调用邮箱接口发送邮件的函数
from django.core.mail import send_mail
# django系统配置(邮件相关配置)
from django.conf import settings
# 页面静态化时使用的商品名称
from goods.models import GoodsCategory, IndexGoodsBanner, IndexPromotionBanner, IndexCategoryGoodsBanner
# 获取需要加载数据的模板对象
from django.template import loader, RequestContext

import os



# 创建celery的应用
# celery_app = Celery()
# 参数1: broker(消息中间人)名字 参数2:任务存储空间(缓存)
app = Celery('dailyfresh', broker='redis://192.168.62.130:6379/0')

# 定义任务
# app.task()是将任务处理函数注册到broker的任务队列中,这时函数变成了一个任务
@app.task
def send_active_email(user_name,active_url,email):
    """
    发送激活邮件
    :param user_name:用户名 字符串
    :param active_url: 激活账户的url 字符串
    :param email: 用户邮箱 字符串
    :return: None
    """
    # 发送激活的邮件
    # send_mail(邮件标题,邮件内容,发件人,收件人,html_message=html格式的邮件内容)
    html_message = """
            <h1>天天生鲜用户激活</h>
            %s
            <a href=%s>%s</a>
            """ % (user_name,active_url, '请点击激活')
    send_mail('天天生鲜', '', settings.EMAIL_FROM, [email], html_message=html_message)

# 页面静态化
@app.task
def generate_static_index_html():
    # 商品的品类
    categories = GoodsCategory.objects.all()
    # 首页轮播图
    index_goods_banners = IndexGoodsBanner.objects.all().order_by("index")[:4]
    # 首页广告活动数据,[]切片,限制数量
    promotion_banners = IndexPromotionBanner.objects.all().order_by("index")[:2]
    # 首页分类商品展示数据
    for category in categories:
        category_goods_title_banners = IndexCategoryGoodsBanner.objects\
                                        .filter(category=category,display_type=0)\
                                        .order_by('index')[:5]
        category.title_banners = category_goods_title_banners
        category_goods_image_banners = IndexCategoryGoodsBanner.objects\
                                        .filter(category=category,display_type=1)\
                                        .order_by('index')[:4]
        category.image_banners = category_goods_image_banners
        # print只接受字符串,当传入对象时,对象会先去调用__str__方法,返回字符串
        # print(category.title_banners)
        # print(category.image_banners)
        # print(category)
        # print('')

    # 模板的数据
    context = {
        'categories': categories,
        'index_goods_banners': index_goods_banners,
        'promotion_banners': promotion_banners,
    }
    # print("context")
    # print(context)
    # context数据内容有:
    #     {
    #         'categories': categories,
    #         'index_goods_banners': index_goods_banners,
    #         'promotion_banners': promotion_banners,
    #         'cart_num': cart_num,
    #     }
    # 优化用户访问时间和降低数据库操作和服务器压力的方法
    # 方法一: 页面静态化步骤
    # 1.运营人员操作admin录入商品数据
    # 2.Django将存储任务发布到celery任务队列中
    # 3.在Celery处理admin站点保存请求的时候,执行生成静态页面的任务
    # 4.将生成的静态页面保存到Nginx服务器中
    # 5.

    #  获取模板
    temp = loader.get_template('index_for_static.html')
    # 构造末班要要到的上下文对象(模板数据对象)
    # 不需要传入request对象,可以直接通过render渲染模板
    # req_context = RequestContext(request,context)
    # 渲染模板
    html_file_data = temp.render(context)

    # 保存生成好的静态文件
    file_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(file_path, 'w') as f:
        f.write(html_file_data)