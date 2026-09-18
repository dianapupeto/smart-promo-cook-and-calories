"""
Пример как се използва service слоят от management команда.
Пуска се напр. от Celery Beat всеки понеделник:
    python manage.py generate_shopping_list --menu-id 3
"""
from collections import defaultdict

from django.core.management.base import BaseCommand, CommandError

from meal_plans.models import WeeklyMenu
from products.models import UserInventory
from promotions.models import Promotion
from shopping.models import ShoppingList, ShoppingListItem


class Command(BaseCommand):
    help = "Генерира списък за пазаруване от одобрено седмично меню, приспадайки наличния инвентар."

    def add_arguments(self, parser):
        parser.add_argument("--menu-id", type=int, required=True)

    def handle(self, *args, **options):
        try:
            menu = WeeklyMenu.objects.get(id=options["menu_id"])
        except WeeklyMenu.DoesNotExist:
            raise CommandError("Меню с това ID не съществува.")

        user = menu.created_by
        if user is None:
            raise CommandError("Менюто няма зададен потребител.")

        # 1. Сумирай нужните количества от всички рецепти в менюто
        needed = defaultdict(float)
        for entry in menu.entries.select_related("recipe").prefetch_related("recipe__ingredients"):
            for ri in entry.recipe.ingredients.all():
                needed[ri.product_id] += float(ri.quantity_grams)

        # 2. Извади наличното в инвентара на потребителя
        inventory = {
            inv.product_id: float(inv.quantity)
            for inv in UserInventory.objects.filter(user=user)
        }

        shopping_list, _ = ShoppingList.objects.get_or_create(
            user=user, menu=menu, week_start=menu.week_start
        )
        shopping_list.items.all().delete()

        active_promos = {
            p.product_id: p
            for p in Promotion.objects.filter(week_start=menu.week_start)
        }

        created = 0
        for product_id, qty_needed in needed.items():
            remaining = qty_needed - inventory.get(product_id, 0)
            if remaining <= 0:
                continue
            promo = active_promos.get(product_id)
            ShoppingListItem.objects.create(
                shopping_list=shopping_list,
                product_id=product_id,
                quantity=remaining,
                from_promotion=promo,
                estimated_price=(promo.promo_price if promo else 0),
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Готово: {created} артикула добавени в списъка за {user.username}."
        ))
