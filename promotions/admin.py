from django.contrib import admin
from .models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        "product", "store", "regular_price", "promo_price",
        "savings_display", "week_start", "week_end",
    )
    list_filter = ("store", "week_start", "product__category")
    search_fields = ("product__name", "store__name")
    autocomplete_fields = ("store", "product")
    date_hierarchy = "week_start"

    @admin.display(description="Спестяване")
    def savings_display(self, obj):
        return f"{obj.savings_amount} лв. ({obj.savings_percent}%)"
