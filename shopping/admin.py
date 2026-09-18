from django.contrib import admin
from .models import ShoppingList, ShoppingListItem


class ShoppingListItemInline(admin.TabularInline):
    model = ShoppingListItem
    extra = 1
    autocomplete_fields = ("product", "from_promotion")


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("user", "week_start", "menu", "total_estimated_price")
    list_filter = ("week_start",)
    search_fields = ("user__username",)
    autocomplete_fields = ("user", "menu")
    inlines = [ShoppingListItemInline]
