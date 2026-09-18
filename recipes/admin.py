from django.contrib import admin
from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ("product",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "servings", "prep_time_minutes", "calories_per_serving_display")
    search_fields = ("title",)
    filter_horizontal = ("dietary_tags",)
    inlines = [RecipeIngredientInline]

    @admin.display(description="Ккал/порция")
    def calories_per_serving_display(self, obj):
        return obj.calories_per_serving
