from django.db import models


class TimeStampedModel(models.Model):
    """Абстрактен базов модел с дати на създаване/промяна — наследяват го всички апове."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
