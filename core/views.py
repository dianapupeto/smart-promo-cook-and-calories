from datetime import date

from django.db.models import Sum
from django.shortcuts import render

from promotions.models import Promotion
from recipes.models import Recipe
from savings.models import SavingsRecord


def home(request):
    """Начална страница: текущи промоции, наскоро добавени рецепти, обща спестена сума."""
    today = date.today()
    current_promotions = (
        Promotion.objects.filter(week_start__lte=today, week_end__gte=today)
        .select_related("store", "product")
        .order_by("-created_at")[:6]
    )
    featured_recipes = Recipe.objects.order_by("-created_at")[:3]

    aggregate = SavingsRecord.objects.aggregate(
        regular=Sum("total_regular_price"), spent=Sum("total_spent")
    )
    total_saved_amount = (aggregate["regular"] or 0) - (aggregate["spent"] or 0)

    context = {
        "current_promotions": current_promotions,
        "featured_recipes": featured_recipes,
        "total_saved_amount": total_saved_amount,
        "promotions_count": current_promotions.count(),
    }
    return render(request, "core/home.html", context)
