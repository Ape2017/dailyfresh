"""
全文检索,商品索引类
"""
# 连接搜索引擎的中间人
from haystack import indexes
# 查询的数据库表
from .models import GoodsSKU


class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    """商品索引类"""
    # 关键词
    text = indexes.CharField(document=True, use_template=True)

    # 返回模型类对象
    def get_model(self):
        return GoodsSKU

    # 返回查询结果集
    def index_queryset(self, using=None):
        # 不过滤操作
        # return self.get_model().objects.filter()
        return self.get_model().objects.all()

