from django import forms
from .models import CategoriaTreino

class FormUpload(forms.ModelForm):
    class Meta:
        model = CategoriaTreino
        fields=  ['imagem']