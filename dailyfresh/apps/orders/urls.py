from django.conf.urls import url
from . import views

urlpatterns = [
    # 用户下单视图类(来源于购物车中的去支付(AJAX)和详情页的立即购买(AJAX))
    url(r"^place$", views.PlaceOrderView.as_view(), name="place"),
    # 用户去支付(来源于用户中心订单的去支付按钮(AJAX)),进入支付页面
    url(r"^commit$", views.CommitOrderView.as_view(), name="commit"),
    # 个人中心的所有订单,来源于用户请求,请求方式get
    url('^(?P<page>\d+)$', views.UserOrdersView.as_view(), name="info"),
    # 商品评论页,请求方式get和post,来源商品详情页和用户中心页
    url('^comment/(?P<order_id>\d+)$', views.CommentView.as_view(), name="comment"),
    # 用户支付页面,请求方式Post(Ajax),来源用户点击去支付后的请求
    url('^pay$', views.PayView.as_view(), name="pay"),
    # 检查支付结果,请求方式get(Ajax),来源于支付页面的发起支付后激发的请求
    url('^check_pay$', views.CheckPayResultView.as_view(), name="check_pay"),
]
