from django import forms
from django.forms import modelformset_factory

from .models import ShoppingListItem


class ShoppingListItemForm(forms.ModelForm):
    """
    Една форма на артикул от списъка. Клиентът само въвежда/потвърждава
    реално купеното количество — всичко останало (продукт, промоция, нужно количество)
    е read-only контекст, зададен от системата/админа.
    """

    class Meta:
        model = ShoppingListItem
        fields = ["quantity_purchased"]
        widgets = {
            "quantity_purchased": forms.NumberInput(attrs={
                "step": "0.01", "min": "0", "class": "qty-input",
            }),
        }
        labels = {"quantity_purchased": ""}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity_purchased"].required = False
        # Ако клиентът не пипне полето, по подразбиране приемаме, че е купил точно нужното.
        if self.instance and self.instance.pk and self.instance.quantity_purchased is None:
            self.fields["quantity_purchased"].initial = self.instance.quantity

    def clean_quantity_purchased(self):
        qty = self.cleaned_data.get("quantity_purchased")
        if qty is None:
            return self.instance.quantity
        if qty < 0:
            raise forms.ValidationError("Количеството не може да е отрицателно число.")
        return qty


ShoppingListItemFormSet = modelformset_factory(
    ShoppingListItem,
    form=ShoppingListItemForm,
    extra=0,
    can_delete=False,
)
