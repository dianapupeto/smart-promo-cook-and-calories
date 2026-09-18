"""
Бизнес логика, която не принадлежи само на един модел.
Държим я отделно от models.py/views.py, за да е лесно тествана и преизползваема
(напр. от Celery задачи, management commands, DRF views).
"""
from django.db.models import Sum, F, Q

from products.models import Product, UserInventory
from promotions.models import Promotion
from recipes.models import Recipe, RecipeIngredient


def find_recipes_for_week(week_start, min_match_ratio: float = 0.6):
    """
    Връща рецепти, чиито продукти в значителна степен (>= min_match_ratio)
    се покриват от активните промоции за седмицата.
    Опростен пример — за production добавете кеширане/агрегации на DB ниво.
    """
    promo_product_ids = set(
        Promotion.objects.filter(week_start=week_start).values_list("product_id", flat=True)
    )
    if not promo_product_ids:
        return Recipe.objects.none()

    matching_ids = []
    for recipe in Recipe.objects.prefetch_related("ingredients__product"):
        ingredient_ids = set(recipe.ingredients.values_list("product_id", flat=True))
        if not ingredient_ids:
            continue
        overlap = len(ingredient_ids & promo_product_ids) / len(ingredient_ids)
        if overlap >= min_match_ratio:
            matching_ids.append(recipe.id)

    return Recipe.objects.filter(id__in=matching_ids)


def recipes_using_leftover_inventory(user):
    """Кои рецепти могат да се сготвят основно с продукти, останали от предишни покупки."""
    inventory_product_ids = set(
        UserInventory.objects.filter(user=user, quantity__gt=0).values_list("product_id", flat=True)
    )
    matches = []
    for recipe in Recipe.objects.prefetch_related("ingredients__product"):
        ingredient_ids = set(recipe.ingredients.values_list("product_id", flat=True))
        if ingredient_ids and ingredient_ids.issubset(inventory_product_ids):
            matches.append(recipe)
    return matches


def suggest_long_shelf_life_promotions(week_start, min_shelf_life_days: int = 30):
    """Промоции на продукти, които си струва да се купят в по-голямо количество."""
    return Promotion.objects.filter(
        week_start=week_start,
        product__default_shelf_life_days__gte=min_shelf_life_days,
    ).select_related("product", "store")


def calculate_recipe_calories(recipe):
    """Сумарни калории на рецепта на база количество от всяка съставка."""
    total = 0
    for ri in recipe.ingredients.select_related("product"):
        total += (ri.product.calories_per_100 or 0) * float(ri.quantity_grams) / 100
    return round(total, 1)
