# -*- coding: utf-8 -*- 
from django import forms
from models import Professor
from disciplinas.models import Disciplina



class ProfessorForm(forms.ModelForm):
    disciplinas = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset= Disciplina.objects.all(),
        required=False 
        )
    label = forms.CharField(max_length=7,
        help_text = "Nome pequeno para melhorar vizualização do horario",
        label = 'Rótulo (Abreviação)')
    def __init__(self,*args, **kwargs):
        usuario = kwargs.pop('usuario',None)
        #instance = kwargs.get('instance',None)

        super(ProfessorForm,self).__init__(*args, **kwargs)
        self.fields['disciplinas'].queryset = Disciplina.objects.filter(user=usuario)
            
            
    class Meta:
        model = Professor
        fields = ('nome', 'label','disciplinas')