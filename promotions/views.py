from datetime import date

from django.shortcuts import render

from stores.models import Store
from .models import Promotion


def promotion_list(request):
    """
    Списък с промоции. По подразбиране показва текущата седмица,
    с възможност за филтриране по магазин и преглед на минали седмици.
    """
    today = date.today()

    promotions = Promotion.objects.select_related("store", "product", "product__category")

    week_start_param = request.GET.get("week_start")
    if week_start_param:
        promotions = promotions.filter(week_start=week_start_param)
    else:
        promotions = promotions.filter(week_start__lte=today, week_end__gte=today)

    store_id = request.GET.get("store")
    if store_id:
        promotions = promotions.filter(store_id=store_id)

    promotions = promotions.order_by("store__name", "product__category__name", "product__name")

    context = {
        "promotions": promotions,
        "stores": Store.objects.filter(is_active=True).order_by("name"),
        "selected_store": int(store_id) if store_id else None,
        "week_start_param": week_start_param,
    }
    return render(request, "promotions/list.html", context)
