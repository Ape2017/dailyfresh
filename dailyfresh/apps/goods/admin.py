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

# 在管理后台注册
admin.site.register(GoodsCategory)
admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexCategoryGoodsBanner)
admin.site.register(IndexPromotionBanner)
