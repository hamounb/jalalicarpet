from django import forms
from .models import *


class FilterForm(forms.Form):
    LTH = "lth"
    HTL = "htl"
    FAV = "fav"
    DEF = "def"
    CHOICES = (
        (DEF, "جدیدترین‌ها"),
        (LTH, "کم به زیاد"),
        (HTL, "زیاد به کم"),
        (FAV, "محبوب‌ترین‌ها"),
    )

    price = forms.CharField(widget=forms.Select(choices=CHOICES, attrs={"class":"form-control", "style":"height: calc(2.4em + .75rem + 2px); color:#255a6c; font-size:medium; font-weight:bold", "onchange":"autoSubmit()"}))
    pattern = forms.ModelMultipleChoiceField(queryset=DesignPatternModel.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"onchange":"autoSubmit()"}), required=False, label="نقش‌ها")
    wate = forms.ModelMultipleChoiceField(queryset=WateModel.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"onchange":"autoSubmit()"}), required=False, label="رج‌ها")


class PriceUpdateForm(forms.Form):
    file = forms.FileField()