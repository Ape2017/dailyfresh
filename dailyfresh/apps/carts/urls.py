from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^add$", views.AddView.as_view(), name="add"),

]
