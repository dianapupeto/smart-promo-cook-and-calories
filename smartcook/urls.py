from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout/password reset
    path("accounts/", include("users.urls")),  # signup

    path("", include("core.urls")),
    path("promotions/", include("promotions.urls")),
    path("recipes/", include("recipes.urls")),
    path("menus/", include("meal_plans.urls")),
    path("shopping/", include("shopping.urls")),
    path("savings/", include("savings.urls")),
    path("comments/", include("comments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
