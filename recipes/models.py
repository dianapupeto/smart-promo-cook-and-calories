from django.db import models
from core.models import TimeStampedModel


class Recipe(TimeStampedModel):
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    servings = models.PositiveSmallIntegerField(default=1)
    prep_time_minutes = models.PositiveIntegerField(default=0)
    dietary_tags = models.ManyToManyField("users.DietaryTag", blank=True, related_name="recipes")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("recipes:detail", args=[self.pk])

    @property
    def total_calories(self):
        from core.services import calculate_recipe_calories
        return calculate_recipe_calories(self)

    @property
    def calories_per_serving(self):
        if not self.servings:
            return 0
        return round(self.total_calories / self.servings, 1)


class RecipeIngredient(models.Model):
    """Through модел между Recipe и Product — позволява лесно добавяне на нови продукти."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT, related_name="used_in_recipes")
    quantity_grams = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Количество в грамове/милилитри/брой (според единицата на продукта)"
    )
    optional = models.BooleanField(default=False)

    class Meta:
        unique_together = ("recipe", "product")

    def __str__(self):
        return f"{self.quantity_grams}{self.product.unit} {self.product.name}"
