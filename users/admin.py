from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, DietaryTag, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ("username", "email", "household_size", "daily_calorie_target", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Smart Cook", {"fields": ("household_size", "daily_calorie_target")}),
    )


@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
