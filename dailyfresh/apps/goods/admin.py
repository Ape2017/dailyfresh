from django.contrib import admin
from goods.models import GoodsCategory,Goods,GoodsSKU,GoodsImage,IndexGoodsBanner,IndexCategoryGoodsBanner,IndexPromotionBanner
# Register your models here.

admin.site.register(GoodsCategory)
admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexCategoryGoodsBanner)
admin.site.register(IndexPromotionBanner)
