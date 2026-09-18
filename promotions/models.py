from django.db import models
from core.models import TimeStampedModel


class Promotion(TimeStampedModel):
    """
    Седмична промоция на продукт в конкретен магазин.
    Админ ги качва всяка седмица; от тук тръгва целият flow:
    промоции -> налични продукти -> рецепти -> меню -> калории -> цена -> спестяване.
    """
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, related_name="promotions")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="promotions")

    regular_price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Обичайна цена")
    promo_price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Промоционална цена")
    unit_quantity = models.DecimalField(
        max_digits=8, decimal_places=2, default=1,
        help_text="Количество, за което важи цената (напр. 1000 за 1кг, ако unit=g)"
    )

    week_start = models.DateField()
    week_end = models.DateField()

    source_url = models.URLField(blank=True, help_text="Линк към брошурата/промоцията на магазина")

    class Meta:
        ordering = ["-week_start"]
        indexes = [models.Index(fields=["week_start", "week_end"])]

    def __str__(self):
        return f"{self.product.name} @ {self.store.name} ({self.week_start})"

    @property
    def savings_amount(self):
        return self.regular_price - self.promo_price

    @property
    def savings_percent(self):
        if self.regular_price == 0:
            return 0
        return round((self.savings_amount / self.regular_price) * 100, 1)

    @property
    def regular_unit_price(self):
        """Редовна цена за 1 единица (грам/мл/брой), не за целия пакет."""
        if not self.unit_quantity:
            return self.regular_price
        return self.regular_price / self.unit_quantity

    @property
    def promo_unit_price(self):
        """Промо цена за 1 единица — ползва се за точно пресмятане при различно закупено количество."""
        if not self.unit_quantity:
            return self.promo_price
        return self.promo_price / self.unit_quantity
