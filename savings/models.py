from django.conf import settings
from django.db import models
from core.models import TimeStampedModel


class SavingsRecord(TimeStampedModel):
    """
    Седмичен запис на реално спестено при закупуване от списък.
    Месечните справки се правят чрез агрегация (Sum) по потребител и месец
    в admin Statistics изгледа или в API.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="savings_records")
    shopping_list = models.OneToOneField(
        "shopping.ShoppingList", on_delete=models.CASCADE, related_name="savings_record"
    )
    week_start = models.DateField()
    total_spent = models.DecimalField(max_digits=9, decimal_places=2)
    total_regular_price = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        ordering = ["-week_start"]

    def __str__(self):
        return f"{self.user.username} — {self.week_start}: {self.amount_saved} лв."

    @property
    def amount_saved(self):
        return self.total_regular_price - self.total_spent

    @property
    def savings_percent(self):
        if self.total_regular_price == 0:
            return 0
        return round((self.amount_saved / self.total_regular_price) * 100, 1)
