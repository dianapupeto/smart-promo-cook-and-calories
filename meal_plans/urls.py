from django.urls import path
from . import views

app_name = "meal_plans"

urlpatterns = [
    path("", views.menu_list, name="list"),
    path("<int:pk>/", views.menu_detail, name="detail"),
]
