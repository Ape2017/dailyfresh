from celery import Celery

# 讲django项目的配置文件信息保存到操作系统中
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dailyfresh.setting'

# 让django初始化一下,django读入配置文件的信息
# django.setup()会询问操作系统配置文件的位置,读入配置文件的信息

# 在启动celery的时候需要,在启动django的时候不需要,需要注释掉
# import django
# django.setup()

# 启动celery的命令
# celery -A celery_task.tasks worker -l info

from django.core.mail import send_mail
from django.conf import settings

# 创建celery的应用
# celery_app = Celery()
app = Celery('dailyfresh', broker='redis://127.0.0.1:6379/0')

# 定义任务
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

