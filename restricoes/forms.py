from django import forms
from models import Restricao

class RestricaoForm(forms.ModelForm):
    
    tipo = forms.ChoiceField(
        widget=forms.Select,
        choices=(
            ("0", "Indisponivel"),
            ("1", "Indesejavel"),
            ("2", "Disponivel"),
        ),
    )
    class Meta:
        model = Restricao
        fields = ('tipo',)