# -*- coding: utf-8 -*-
from django import forms
from models import Grade

class GradeForm(forms.ModelForm):
    dias = forms.IntegerField(label = 'Dias Letivos',
        help_text = "Quantidade de dias letivos da semana",
        initial = 5)
    auladia = forms.IntegerField(label = 'Aulas por Dia',
        help_text = "Quantidade de aulas por dia",
        initial = 5)
    ano = forms.IntegerField(label = 'Ano',
        help_text = "Ano letivo",
        initial = 2013)
    periodo = forms.IntegerField(label = 'Período',
        help_text = "Período",
        initial = 1)
    class Meta:
        model = Grade
        fields = ('escola', 'turno','dias','auladia','ano','periodo')
