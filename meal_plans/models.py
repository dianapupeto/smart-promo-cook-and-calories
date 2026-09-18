from django.conf import settings
from django.db import models
from core.models import TimeStampedModel


class WeeklyMenu(TimeStampedModel):
    STATUS_CHOICES = [
        ("draft", "Чернова"),
        ("pending", "Чака одобрение"),
        ("approved", "Одобрено"),
        ("rejected", "Отхвърлено"),
    ]

    title = models.CharField(max_length=150, blank=True)
    week_start = models.DateField()
    week_end = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="menus"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ["-week_start"]

    def __str__(self):
        return self.title or f"Меню {self.week_start} - {self.week_end}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("meal_plans:detail", args=[self.pk])


class MenuEntry(models.Model):
    DAY_CHOICES = [
        ("mon", "Понеделник"), ("tue", "Вторник"), ("wed", "Сряда"),
        ("thu", "Четвъртък"), ("fri", "Петък"), ("sat", "Събота"), ("sun", "Неделя"),
    ]
    MEAL_TYPE_CHOICES = [
        ("breakfast", "Закуска"), ("lunch", "Обяд"), ("dinner", "Вечеря"), ("snack", "Междинно"),
    ]

    menu = models.ForeignKey(WeeklyMenu, on_delete=models.CASCADE, related_name="entries")
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.PROTECT, related_name="menu_entries")
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)

    class Meta:
        ordering = ["day", "meal_type"]

    def __str__(self):
        return f"{self.get_day_display()} {self.get_meal_type_display()}: {self.recipe.title}"
