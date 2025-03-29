from django import forms
from .models import *


class FilterForm(forms.Form):
    LTH = "lth"
    HTL = "htl"
    FAV = "fav"
    DEF = "def"
    CHOICES = (
        (DEF, "جدیدترین‌ها"),
        (LTH, "ارزانترین‌ها"),
        (HTL, "گرانترین‌ها"),
        (FAV, "محبوب‌ترین‌ها"),
    )

    price = forms.CharField(widget=forms.RadioSelect(choices=CHOICES, attrs={ "onchange":"autoSubmit()"}), required=False)
    # price = forms.CharField(widget=forms.Select(choices=CHOICES, attrs={"class":"form-control", "style":"height: calc(2.4em + .75rem + 2px); color:#255a6c; font-size:medium; font-weight:bold", "onchange":"autoSubmit()"}))
    pattern = forms.ModelMultipleChoiceField(queryset=DesignPatternModel.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"onchange":"autoSubmit()"}), required=False, label="نقش‌ها")
    wate = forms.ModelMultipleChoiceField(queryset=WateModel.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"onchange":"autoSubmit()"}), required=False, label="رج‌ها")


class PriceUpdateForm(forms.Form):
    file = forms.FileField()


class HeaderSearchForm(forms.Form):
    query = forms.CharField(max_length=255, label="جستجو", widget=forms.TextInput(attrs={"class":"form-control text-1", "placeholder":"جستجو ..."}))