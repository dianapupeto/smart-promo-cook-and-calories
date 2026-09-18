from django.contrib import admin
from .models import WeeklyMenu, MenuEntry


class MenuEntryInline(admin.TabularInline):
    model = MenuEntry
    extra = 1
    autocomplete_fields = ("recipe",)


@admin.register(WeeklyMenu)
class WeeklyMenuAdmin(admin.ModelAdmin):
    list_display = ("__str__", "week_start", "week_end", "status", "created_by")
    list_filter = ("status", "week_start")
    search_fields = ("title",)
    inlines = [MenuEntryInline]
    autocomplete_fields = ("created_by",)
