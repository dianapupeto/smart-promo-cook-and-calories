from django.db import models
from core.models import TimeStampedModel


class Store(TimeStampedModel):
    """Голям хранителен магазин/верига (Kaufland, Lidl, Billa...)."""
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="stores/logos/", blank=True, null=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StoreBranch(models.Model):
    """По желание — конкретен обект/адрес, ако проследявате промоции по локация."""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="branches")
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.store.name} - {self.city}"
