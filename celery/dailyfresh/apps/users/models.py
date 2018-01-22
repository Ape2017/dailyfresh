# django数据库包
from django.db import models
# django用户认证包
from django.contrib.auth.models import AbstractUser
# 自定义的公用基础模块的基础模型类,用于创建用户注册时间和修改内容的时间,公用模块
from utils.models import BaseModel
# token令牌包,用于用户生成token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# 项目配置模块
from django.conf import settings
# 常量包,用于导入常量USER_ACTIVE_EXPIRES(用户账户激活邮件链接的有效期)
from utils import constants


class User(AbstractUser, BaseModel):
    """用户模型类,继承系统的用户管理系统类,抽象基础类"""
    class Meta:
        # 定义数据表名字,和数据库解耦
        db_table = "df_users"

    def generate_active_token(self):
        """生成用户激活的令牌"""
        # 创建序列化工具对象
        # 对象s 参数1:秘钥 2:失效时间
        s = Serializer(settings.SECRET_KEY,constants.USER_ACTIVE_EXPIRES )
        # dumps()方法将数据序列化为字符串  参数:格式字典 信息 返回值:(b'') 类型:二进制字节码字串(包含数据,穿件时间)
        # decode()方法,将字节型字符串转换为字符串类型 参数:空 返回值:字符串
        # 必须将字节码转成字符串,需要拼接超链接,字节码前面有带标示b
        token = s.dumps({'user_id':self.id}).decode()
        return token


class Address(BaseModel):
    """ORM收货地址模型类"""
    # 用户id
    user = models.ForeignKey(User, verbose_name="所属用户")
    # 收件人
    receiver_name = models.CharField(max_length=20, verbose_name="收件人")
    # 手机号
    receiver_mobile = models.CharField(max_length=11, verbose_name="联系电话")
    # 收件地址
    detail_addr = models.CharField(max_length=256, verbose_name="详细地址")
    # 邮编
    zip_code = models.CharField(max_length=6, verbose_name="邮政编码")

    class Meta:
        # 定义数据表名字, 和数据库解耦
        db_table = "df_address"



