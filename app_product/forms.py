from django import forms

from app_category.models import CategoryModel

class ProductEditForm(forms.Form):
    image = forms.ImageField(required=False)
    name = forms.CharField()
    price = forms.IntegerField()
    unity = forms.ChoiceField(choices=[('dona', 'dona'), ('kg', 'kg')])
    count = forms.IntegerField()

    category = forms.ModelMultipleChoiceField(
        queryset=CategoryModel.objects.all(),  # barcha kategoriyalar
        widget=forms.SelectMultiple(attrs={"class": "form-select", "multiple": "multiple"})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # view dan user uzatiladi
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = CategoryModel.objects.filter(user=user)

