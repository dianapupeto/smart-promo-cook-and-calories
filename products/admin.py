from django.contrib import admin
from .models import Category, Product, ProductStorageInfo, UserInventory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)


class ProductStorageInfoInline(admin.StackedInline):
    model = ProductStorageInfo
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "unit", "calories_per_100", "default_shelf_life_days")
    list_filter = ("category", "unit")
    search_fields = ("name",)
    filter_horizontal = ("dietary_tags",)
    inlines = [ProductStorageInfoInline]


@admin.register(UserInventory)
class UserInventoryAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "source", "purchase_date", "expiry_date")
    list_filter = ("source", "expiry_date")
    search_fields = ("user__username", "product__name")
    autocomplete_fields = ("user", "product")
