# Smart Cook — Django backbone

Скелет на проекта, готов за разширение. Django не е инсталиран в средата,
в която е генериран този код — не е тестван с `runserver`, но е синтактично
валиден (`python -m py_compile`) и следва стандартна Django структура.

## Стартиране

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Админ панелът е на `/admin/`.

## Структура на приложенията

| App | Отговорност |
|---|---|
| `core` | Абстрактен `TimeStampedModel` + `services.py` с бизнес логика (matching на рецепти с промоции, препоръки за дълготрайни продукти, калкулация на калории) |
| `users` | Custom `User`, `DietaryTag`, `UserProfile` |
| `stores` | `Store`, `StoreBranch` |
| `products` | `Category`, `Product`, `ProductStorageInfo` (как да се съхрани), `UserInventory` (останали продукти) |
| `promotions` | `Promotion` — седмични промоции, `savings_amount`/`savings_percent` |
| `recipes` | `Recipe`, `RecipeIngredient` (with калории през `core.services`) |
| `meal_plans` | `WeeklyMenu`, `MenuEntry` |
| `shopping` | `ShoppingList`, `ShoppingListItem` + management команда `generate_shopping_list` |
| `savings` | `SavingsRecord` — реално спестено на седмица/месец |
| `comments` | `Comment` (generic, за рецепти/менюта), `MenuSubmission` (потребителски предложения, чакащи одобрение) |

## Следващи стъпки

1. `python manage.py makemigrations && migrate` — генерирайте първите миграции.
2. Публично front-end: добавете `templates/` + views (или DRF + отделен frontend).
3. `core/services.py` съдържа основната matching логика — тества се лесно изолирано от views.
4. Добавете Celery + Celery Beat за:
   - седмично автоматично `generate_shopping_list`
   - напомняния за изтичащи продукти в `UserInventory`
5. Смяна на SQLite → PostgreSQL за продукция (виж коментара в `settings.py`).
6. Admin "Statistics" изглед — добавете custom admin view (не модел), който агрегира
   `SavingsRecord` по месец/потребител с `annotate`/`aggregate`.
7. За API — добавете `djangorestframework` (вече е в requirements.txt) и сериализатори
   за всеки модел.

## Демонстрационен flow

```
Promotion (admin качва седмично)
  -> core.services.find_recipes_for_week()
  -> WeeklyMenu / MenuEntry (одобрено меню)
  -> shopping.management.commands.generate_shopping_list --menu-id N
  -> ShoppingList / ShoppingListItem (само липсващото от UserInventory)
  -> SavingsRecord (регулярна цена - платена цена)
```
