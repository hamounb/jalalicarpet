from django import forms
from .models import ContactUsModel

class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUsModel
        fields = '__all__'