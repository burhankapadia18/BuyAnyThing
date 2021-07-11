from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="shopHome"),
    path("contact/", views.contact, name="contactUs"),
    path("about/", views.about, name="aboutUs"),
    path("tracker/", views.tracker, name="trackingStatus"),
    path("search", views.search, name="search"),
    path("productView/<int:pid>", views.prodView, name="productView"),
    path("checkout/", views.checkout, name="checkout"),
]