from django.contrib import admin
from .models import SavingsRecord


@admin.register(SavingsRecord)
class SavingsRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "week_start", "total_spent", "total_regular_price", "amount_saved_display")
    list_filter = ("week_start",)
    autocomplete_fields = ("user", "shopping_list")

    @admin.display(description="Спестено")
    def amount_saved_display(self, obj):
        return f"{obj.amount_saved} лв. ({obj.savings_percent}%)"
