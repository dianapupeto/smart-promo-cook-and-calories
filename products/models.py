from django.conf import settings
from django.db import models
from core.models import TimeStampedModel


class Category(models.Model):
    """Месо, млечни, зеленчуци, консерви, подправки..."""
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    UNIT_CHOICES = [
        ("g", "грам"),
        ("ml", "милилитър"),
        ("pcs", "брой"),
    ]

    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="g")
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    # Хранителна стойност на 100 г/мл (или на брой, ако unit=pcs)
    calories_per_100 = models.PositiveIntegerField(default=0)
    protein_per_100 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fat_per_100 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbs_per_100 = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # Използва се за препоръка "купи за по-дълго", когато е на промоция
    default_shelf_life_days = models.PositiveIntegerField(
        default=7, help_text="Типичен срок на годност при нормално съхранение (дни)"
    )
    dietary_tags = models.ManyToManyField("users.DietaryTag", blank=True, related_name="products")

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "category")

    def __str__(self):
        return self.name


class ProductStorageInfo(models.Model):
    """Как да се съхрани продукт за по-нататъшна употреба, когато няма промоция."""
    STORAGE_TYPE_CHOICES = [
        ("fresh", "Свежо / хладилник"),
        ("frozen", "Замразяване"),
        ("canned", "Консервиране"),
        ("dry", "Сухо съхранение"),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="storage_info")
    storage_type = models.CharField(max_length=10, choices=STORAGE_TYPE_CHOICES)
    shelf_life_days_when_stored = models.PositiveIntegerField(
        help_text="Срок на годност при това съхранение (напр. замразено)"
    )
    tips = models.TextField(blank=True, help_text="Кратки съвети за съхранение")

    def __str__(self):
        return f"{self.product.name} — {self.get_storage_type_display()}"


class UserInventory(models.Model):
    """
    Какво е останало у потребителя от предишни покупки/готвения.
    Основа за откриване на 'останали продукти' и за автоматично приспадане
    от списъка за пазаруване.
    """
    SOURCE_CHOICES = [
        ("promotion", "Купено на промоция"),
        ("regular", "Купено на редовна цена"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inventory")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory_entries")
    quantity = models.DecimalField(max_digits=8, decimal_places=2, help_text="В единицата на продукта")
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default="regular")
    purchase_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "User inventories"
        ordering = ["expiry_date"]

    def __str__(self):
        return f"{self.user.username}: {self.quantity}{self.product.unit} {self.product.name}"
