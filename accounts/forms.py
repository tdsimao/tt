# -*- coding: utf-8 -*- 
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class MyRegistrarionForm(UserCreationForm):
    email = forms.EmailField(required = True)
    criarDisciplinasPadrao = forms.BooleanField( label="Cadastrar conjunto de Disciplinas padrão",initial = True)
    class Meta:
        model = User
        fields = ('username','email', 'password1','password2','first_name','last_name', 'criarDisciplinasPadrao')
    
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name')
    
    