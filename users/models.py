from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user — позволява лесно разширение (домакинство, диета) без миграция по-късно."""
    household_size = models.PositiveSmallIntegerField(default=1)
    daily_calorie_target = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username


class DietaryTag(models.Model):
    """Напр. vegan, gluten-free, без ядки — ползва се и от Product, и от User."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    dietary_tags = models.ManyToManyField(DietaryTag, blank=True, related_name="users")
    preferred_stores = models.ManyToManyField("stores.Store", blank=True, related_name="preferred_by")

    def __str__(self):
        return f"Profile: {self.user.username}"
