# 数据库路由模型类
class MasterSlaveRouter(object):
    """读写分离路由"""

    def db_for_read(self, model, **hints):
        """
        读数据时访问的数据库
        :param model:
        :param hints:
        :return:
        """

        return "slave"

    def db_for_write(self, model, **hints):
        """写数据时访问的数据库"""
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """是否允许关联查询"""
        return True
