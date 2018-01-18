from django.conf.urls import url
from . import views

urlpatterns = [

    url(r"^porder$", views.POrder.as_view(), name="porder"),

]
