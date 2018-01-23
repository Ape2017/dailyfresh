from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^add$", views.AddView.as_view(), name="add"),
    url(r"^info$", views.InfoView.as_view(), name="info"),
    url(r"^update$", views.UpdateView.as_view(), name="update"),
    url(r"^delete", views.DeleteView.as_view(), name="delete"),

]
