from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, MenuSubmissionForm
from .models import MenuSubmission


@login_required
def add_comment(request, app_label, model_name, object_id):
    """
    Generic endpoint за добавяне на коментар към произволен модел
    (рецепта, седмично меню и т.н.), реферирано по app_label/model_name/pk.
    """
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    target_object = get_object_or_404(content_type.model_class(), pk=object_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = object_id
            comment.save()
            messages.success(request, "Коментарът е добавен.")
        else:
            messages.error(request, "Коментарът не можа да се запази — провери въведеното.")

    return redirect(target_object.get_absolute_url() if hasattr(target_object, "get_absolute_url") else "/")


@login_required
def submit_menu(request):
    """Потребителят предлага меню за одобрение от админ (MenuSubmission, status='pending')."""
    if request.method == "POST":
        form = MenuSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            form.save_m2m()
            messages.success(request, "Менюто е изпратено за преглед. Ще получиш обратна връзка скоро.")
            return redirect("comments:my_submissions")
    else:
        form = MenuSubmissionForm()

    return render(request, "comments/submit_menu.html", {"form": form})


@login_required
def my_submissions(request):
    submissions = MenuSubmission.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "comments/my_submissions.html", {"submissions": submissions})
