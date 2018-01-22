# django系统自带数据库管理模块
from django.db import models


class BaseModel(models.Model):
    """为模型类补充字段"""
    # 数据添加时间(唯一,不能更改)
    #参数auto_now表示每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳，它总是使用当前日期，默认为false
    # 参数auto_now_add表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为false
    # 参数auto_now_add和auto_now是相互排斥的，组合将会发生错误
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 数据最后修改时间(每次修改的时间)
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 说明是抽象模型类

