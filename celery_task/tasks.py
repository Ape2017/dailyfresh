# 受django委托发送邮件方 celery(分布式任务队列)
from celery import Celery
# 将django项目的配置文件信息保存到操作系统中
import sys
sys.path.append('../dailyfresh/dailyfresh.settings')
print(sys.path)
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dailyfresh.settings'
# 在启动celery的时候需要，在启动django的时候不需要，需要注释掉
# 让django初始化一下，django读入配置文件的信息
# django.setup()会询问操作系统配置文件的位置，读入配置文件的信息
# 以下两行在启动celery时打开注释,启动Django时注释
import django
django.setup()
# 启动celery的命令
# celery -A celery_task.tasks worker -l info
# django系统调用邮箱接口发送邮件的函数
from django.core.mail import send_mail
# django系统配置(邮件相关配置)
from django.conf import settings

# 创建celery的应用
# celery_app = Celery()
# 参数1: broker(消息中间人)名字 参数2:任务存储空间(缓存)
app = Celery('dailyfresh', broker='redis://127.0.0.1:6379/0')

# 定义任务
# app.task()是将任务处理函数注册到broker的任务队列中,这时函数变成了一个任务
@app.task()
def send_active_email(user_name,active_url,email):
    """
    发送激活邮件
    :param user_name:用户名
    :param active_url: 激活账户的url
    :param email: 用户邮箱
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

