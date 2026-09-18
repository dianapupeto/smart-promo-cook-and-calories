from django.conf import settings
from django.db import models
from core.models import TimeStampedModel


class ShoppingList(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shopping_lists")
    menu = models.ForeignKey(
        "meal_plans.WeeklyMenu", on_delete=models.SET_NULL, null=True, blank=True, related_name="shopping_lists"
    )
    week_start = models.DateField()

    def __str__(self):
        return f"Списък {self.user.username} — {self.week_start}"

    @property
    def total_estimated_price(self):
        return sum(item.estimated_price for item in self.items.all())


class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT, related_name="shopping_items")
    quantity = models.DecimalField(max_digits=8, decimal_places=2, help_text="Нужно количество за менюто")
    quantity_purchased = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Реално закупено количество. Ако е повече от нужното (напр. по-голям промо пакет), "
                   "разликата автоматично отива в инвентара при финализиране на пазаруването."
    )
    from_promotion = models.ForeignKey(
        "promotions.Promotion", on_delete=models.SET_NULL, null=True, blank=True, related_name="shopping_items"
    )
    estimated_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity}{self.product.unit} {self.product.name}"
