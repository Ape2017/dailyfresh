from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^list$", views.ListView.as_view(), name="list"),
    url(r"^porder$", views.POrder.as_view(), name="porder"),

]
