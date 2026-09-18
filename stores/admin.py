from django.contrib import admin
from .models import Store, StoreBranch


class StoreBranchInline(admin.TabularInline):
    model = StoreBranch
    extra = 1


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    inlines = [StoreBranchInline]
