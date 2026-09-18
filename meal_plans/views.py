from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render

from comments.forms import CommentForm
from comments.models import Comment
from .models import WeeklyMenu, MenuEntry

DAY_ORDER = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DAY_LABELS = dict(MenuEntry.DAY_CHOICES)


def menu_list(request):
    """Показва само одобрените менюта — чернови/чакащи одобрение не са публични."""
    menus = WeeklyMenu.objects.filter(status="approved").order_by("-week_start")
    return render(request, "meal_plans/list.html", {"menus": menus})


def menu_detail(request, pk):
    menu = get_object_or_404(WeeklyMenu.objects.prefetch_related("entries__recipe"), pk=pk)

    by_day = OrderedDict((day, []) for day in DAY_ORDER)
    total_calories = 0
    for entry in menu.entries.all():
        by_day.setdefault(entry.day, []).append(entry)
        total_calories += entry.recipe.calories_per_serving

    content_type = ContentType.objects.get_for_model(WeeklyMenu)
    comments = Comment.objects.filter(
        content_type=content_type, object_id=menu.pk, is_approved=True
    ).select_related("user").order_by("-created_at")

    days_with_entries = [
        (day, DAY_LABELS.get(day, day), entries) for day, entries in by_day.items() if entries
    ]

    context = {
        "menu": menu,
        "days_with_entries": days_with_entries,
        "total_calories": total_calories,
        "comments": comments,
        "comment_form": CommentForm(),
    }
    return render(request, "meal_plans/detail.html", context)
