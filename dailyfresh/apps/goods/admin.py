from django.contrib import admin
from .models import GoodsCategory
from .models import Goods
from .models import GoodsSKU
from .models import GoodsImage
from .models import IndexGoodsBanner
from .models import IndexCategoryGoodsBanner
from .models import IndexPromotionBanner


admin.site.register(GoodsCategory)
admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexCategoryGoodsBanner)
admin.site.register(IndexPromotionBanner)
