from django.urls import path
from . import views

app_name = "shopping"

urlpatterns = [
    path("my-list/", views.my_shopping_list, name="my_list"),
    path("list/<int:list_id>/finish/", views.finish_shopping, name="finish_shopping"),
]
