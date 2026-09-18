from django import forms
from .models import Comment, MenuSubmission


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "rating"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Сподели мнение, колко си спестил/а, или предложение за подобрение…",
            }),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }
        labels = {"content": "Коментар", "rating": "Оценка (1–5, по желание)"}


class MenuSubmissionForm(forms.ModelForm):
    class Meta:
        model = MenuSubmission
        fields = ["title", "week_start", "proposed_recipes", "note"]
        widgets = {
            "week_start": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "title": "Заглавие на менюто",
            "week_start": "Седмица (начална дата)",
            "proposed_recipes": "Рецепти в менюто",
            "note": "Съобщение към екипа (по желание)",
        }
