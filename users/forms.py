from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Имейл")
    household_size = forms.IntegerField(
        min_value=1, initial=1, required=False,
        label="Брой хора в домакинството",
        help_text="Използва се за оразмеряване на количествата в списъка за пазаруване.",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "household_size")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if self.cleaned_data.get("household_size"):
            user.household_size = self.cleaned_data["household_size"]
        if commit:
            user.save()
        return user
