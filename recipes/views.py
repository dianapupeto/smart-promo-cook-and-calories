from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render

from comments.forms import CommentForm
from comments.models import Comment
from users.models import DietaryTag
from .models import Recipe


def recipe_list(request):
    """Списък с рецепти, филтрируем по диетичен таг (vegan, gluten-free...)."""
    recipes = Recipe.objects.all().order_by("title")

    tag_id = request.GET.get("tag")
    if tag_id:
        recipes = recipes.filter(dietary_tags__id=tag_id)

    context = {
        "recipes": recipes,
        "tags": DietaryTag.objects.all(),
        "selected_tag": int(tag_id) if tag_id else None,
    }
    return render(request, "recipes/list.html", context)


def recipe_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related("ingredients__product", "dietary_tags"), pk=pk
    )
    content_type = ContentType.objects.get_for_model(Recipe)
    comments = Comment.objects.filter(
        content_type=content_type, object_id=recipe.pk, is_approved=True
    ).select_related("user").order_by("-created_at")

    context = {
        "recipe": recipe,
        "comments": comments,
        "comment_form": CommentForm(),
        "content_type_name": content_type.model,
    }
    return render(request, "recipes/detail.html", context)
