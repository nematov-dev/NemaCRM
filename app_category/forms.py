from django import forms

class CategoryEditForm(forms.Form):
    name = forms.CharField()