from django.contrib import admin # django核心模块
# 商品类别表
from .models import GoodsCategory
# 商品SPU表
from .models import Goods
# 商品SKU表
from .models import GoodsSKU
# 商品图片
from .models import GoodsImage
# 主页轮播商品展示
from .models import IndexGoodsBanner
# 主页分类商品展示,枚举
from .models import IndexCategoryGoodsBanner
# 主页促销活动展示
from .models import IndexPromotionBanner
# 主页缓存对象,用于清空缓存
from django.core.cache import cache


# 页面静态化的任务发布
class BaseAdmin(admin.ModelAdmin):
    """商品分类admin站点管理类,数据更改时发布页面静态化任务"""
    def save_model(self, request, obj, form, change):
        """当通过admin站点保存模型类数据的时候,被Django调用"""
        # 将模型类对象数据保存到数据库中
        obj.save()
        # 通过celery执行页面静态化的任务
        # 将导包放在这里是celrey初始化时任务还没发布,必须放在这里
        from celery_task.tasks import generate_static_index_html
        # 补充发布生产静态文件的celery任务(异步任务)
        generate_static_index_html.delay()

        # 在更新数据库数据的时候,同步修改缓存数据,(删除)
        cache.delete('index_data')

    def delete_model(self, request, obj):
        """当通过admin站点删除模型类数据的时候,被Django调用"""
        # 将模型类对象数据从数据库中删除
        obj.delete()
        # 通过celery执行页面静态化的任务
        # 将导包放在这里是celrey初始化时任务还没发布,必须放在这里
        from celery_task.tasks import generate_static_index_html
        # 补充发布生产静态文件的celery任务(异步任务)
        generate_static_index_html.delay()

        # 在更新数据库数据的时候,同步修改缓存数据,(删除)
        cache.delete('index_data')


# 页面静态化的任务发布
class GoodsCategoryAdmin(BaseAdmin):
    """商品分类admin站点管理类"""
    pass


class IndexGoodsBannerAdmin(BaseAdmin):
    """主页轮播商品admin站点管理类"""
    pass


class IndexCategoryGoodsBannerAdmin(BaseAdmin):
    """主页分类商品展示admin站点管理类"""
    pass


class IndexPromotionBannerAdmin(BaseAdmin):
    """主页促销活动展示admin站点管理类"""
    pass


# 在管理后台注册
admin.site.register(GoodsCategory, GoodsCategoryAdmin)
admin.site.register(Goods)
admin.site.register(GoodsSKU,GoodsCategoryAdmin)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexCategoryGoodsBanner, IndexCategoryGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
