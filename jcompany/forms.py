from django import forms
from .models import ContactUsModel, FooterNewsModel

class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUsModel
        fields = '__all__'


class FooterNewsForm(forms.ModelForm):

    class Meta:
        model = FooterNewsModel
        fields = ["text"]