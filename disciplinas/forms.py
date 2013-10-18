# -*- coding: utf-8 -*-
from django import forms
from models import Disciplina
from professores.models import Professor

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ('nome', 'label')
    label = forms.CharField(max_length=7,
        help_text = "Nome pequeno para melhorar vizualização do horario")
    professor_set = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset= Professor.objects.all(),
        required=False ,
        label = "Professores habilitados"
        )
    
    def __init__(self,*args, **kwargs):
        usuario = kwargs.pop('usuario',None)
        #instance = kwargs.get('instance',None)

            
        super(DisciplinaForm,self).__init__(*args, **kwargs)
        self.fields['professor_set'].queryset = Professor.objects.filter(user=usuario)
        if 'instance' in kwargs:
            self.fields['professor_set'].initial = kwargs['instance'].professor_set.values_list('id', flat=True).order_by('id')


    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.professor_set.clear()
            for professor in self.cleaned_data['professor_set']:
                instance.professor_set.add(professor)
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance