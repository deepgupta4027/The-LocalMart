from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("basic/", views.basic, name="Basic"),  # make sure this line matches the function
    path("about/", views.about, name="AboutUs"),
    path("tracker/", views.tracker, name="tracker"),
    path("contact/", views.contact, name="contact"),
    path("products/<int:myid>", views.productView, name="productView"),
    path("search/", views.search, name="search"),
    path("checkout/", views.checkout, name="checkout"),
    # path("handlerequest/", views.handlerequest, name="Handlerequest"),
]
