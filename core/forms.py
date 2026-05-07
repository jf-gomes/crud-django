from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['titulo', 'descricao'] # o campo autor não precisa ser incluído, pois será o mesmo do usuário logado.