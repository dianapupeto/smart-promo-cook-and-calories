from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("add/<str:app_label>/<str:model_name>/<int:object_id>/", views.add_comment, name="add"),
    path("submit-menu/", views.submit_menu, name="submit_menu"),
    path("my-submissions/", views.my_submissions, name="my_submissions"),
]
