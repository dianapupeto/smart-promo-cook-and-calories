from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from core.models import TimeStampedModel


class Comment(TimeStampedModel):
    """
    Generic коментар — може да се закачи към Recipe, WeeklyMenu и т.н.
    без нужда от отделен модел за всеки случай.
    Ползва се и за 'колко съм спестил/а', и за общи мнения.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True, blank=True, help_text="1-5, по желание")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    is_approved = models.BooleanField(default=True, help_text="Модерация — скрий неподходящи коментари")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.content[:40]}"


class MenuSubmission(TimeStampedModel):
    """
    Потребителско предложение за меню, чакащо одобрение от админ,
    преди да стане официален WeeklyMenu.
    """
    STATUS_CHOICES = [
        ("pending", "Чака преглед"),
        ("approved", "Одобрено"),
        ("rejected", "Отхвърлено"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="menu_submissions")
    title = models.CharField(max_length=150)
    week_start = models.DateField()
    proposed_recipes = models.ManyToManyField("recipes.Recipe", related_name="submissions", blank=True)
    note = models.TextField(blank=True, help_text="Съобщение от потребителя")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(blank=True, help_text="Обратна връзка от админа")

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
