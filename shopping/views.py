from datetime import date, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import UserInventory
from savings.models import SavingsRecord
from .forms import ShoppingListItemFormSet
from .models import ShoppingList


@login_required
def my_shopping_list(request):
    """
    Показва най-новия списък за пазаруване на текущия потребител, заедно с formset
    за потвърждаване на реално купените количества (валидиран от Django, не ръчно).
    """
    shopping_list = (
        ShoppingList.objects.filter(user=request.user)
        .prefetch_related("items__product", "items__from_promotion")
        .order_by("-week_start")
        .first()
    )

    regular_total = Decimal("0")
    promo_total = Decimal("0")
    formset = None

    if shopping_list:
        items = shopping_list.items.select_related("product", "from_promotion").all()
        for item in items:
            promo_total += item.estimated_price
            if item.from_promotion:
                regular_total += item.from_promotion.regular_unit_price * item.quantity
            else:
                regular_total += item.estimated_price
        formset = ShoppingListItemFormSet(queryset=items, prefix="items")

    savings_record = getattr(shopping_list, "savings_record", None) if shopping_list else None

    context = {
        "shopping_list": shopping_list,
        "formset": formset,
        "regular_total": regular_total,
        "promo_total": promo_total,
        "potential_savings": regular_total - promo_total,
        "savings_record": savings_record,
    }
    return render(request, "shopping/my_list.html", context)


@login_required
def finish_shopping(request, list_id):
    """
    Клиентът потвърждава какво реално е купил (валидирано през ShoppingListItemFormSet).
    От тук нататък системата, а не админът, решава:
      - колко реално е платено спрямо редовните цени -> SavingsRecord
      - какво е купено в повече (напр. по-голям промо пакет) -> отива в UserInventory
        като продукт, останал за следваща употреба.
    """
    shopping_list = get_object_or_404(ShoppingList, id=list_id, user=request.user)
    items = shopping_list.items.select_related("product", "from_promotion").all()

    if request.method != "POST":
        return redirect("shopping:my_list")

    formset = ShoppingListItemFormSet(request.POST, queryset=items, prefix="items")

    if not formset.is_valid():
        messages.error(request, "Провери въведените количества — има грешки във формата.")
        return render(request, "shopping/my_list.html", {
            "shopping_list": shopping_list, "formset": formset,
        })

    total_spent = Decimal("0")
    total_regular = Decimal("0")
    today = date.today()

    for form in formset:
        item = form.instance
        qty_purchased = form.cleaned_data["quantity_purchased"]

        item.quantity_purchased = qty_purchased
        item.purchased = qty_purchased > 0
        item.save(update_fields=["quantity_purchased", "purchased"])

        if qty_purchased <= 0:
            continue

        if item.from_promotion:
            unit_promo = item.from_promotion.promo_unit_price
            unit_regular = item.from_promotion.regular_unit_price
        else:
            unit_price = (item.estimated_price / item.quantity) if item.quantity else Decimal("0")
            unit_promo = unit_regular = unit_price

        total_spent += unit_promo * qty_purchased
        total_regular += unit_regular * qty_purchased

        # Купено в повече от нужното за менюто -> остава за по-нататъшна употреба.
        surplus = qty_purchased - item.quantity
        if surplus > 0:
            shelf_life = getattr(
                getattr(item.product, "storage_info", None), "shelf_life_days_when_stored", None
            ) or item.product.default_shelf_life_days
            UserInventory.objects.create(
                user=request.user,
                product=item.product,
                quantity=surplus,
                source="promotion" if item.from_promotion else "regular",
                purchase_date=today,
                expiry_date=today + timedelta(days=shelf_life),
            )

    SavingsRecord.objects.update_or_create(
        shopping_list=shopping_list,
        defaults={
            "user": request.user,
            "week_start": shopping_list.week_start,
            "total_spent": total_spent,
            "total_regular_price": total_regular,
        },
    )

    messages.success(
        request,
        f"Пазаруването е потвърдено. Спестени {total_regular - total_spent} лв. тази седмица — "
        f"вижте ги в 'Спестявания'."
    )
    return redirect("shopping:my_list")
