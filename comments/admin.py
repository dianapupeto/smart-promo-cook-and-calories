from django.contrib import admin
from .models import Comment, MenuSubmission


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "content_object", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "content_type")
    search_fields = ("content", "user__username")
    autocomplete_fields = ("user",)


@admin.register(MenuSubmission)
class MenuSubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "week_start", "status", "created_at")
    list_filter = ("status", "week_start")
    filter_horizontal = ("proposed_recipes",)
    autocomplete_fields = ("user",)
    actions = ["approve_submissions", "reject_submissions"]

    @admin.action(description="Одобри избраните предложения")
    def approve_submissions(self, request, queryset):
        updated = queryset.update(status="approved")
        self.message_user(request, f"{updated} предложения бяха одобрени.")

    @admin.action(description="Отхвърли избраните предложения")
    def reject_submissions(self, request, queryset):
        updated = queryset.update(status="rejected")
        self.message_user(request, f"{updated} предложения бяха отхвърлени.")
