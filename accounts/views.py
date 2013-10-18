# -*- coding: UTF8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import MyRegistrarionForm, MyUserChangeForm
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from disciplinas.models import Disciplina
from src.variaveisGlobais import disciplinasPadrao



def  login(request):
    c = {}
    c.update(csrf(request))
    context = RequestContext(request,c)
    return render_to_response('login.html',context)

def  auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username = username,  password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin/')
    else:
        return HttpResponseRedirect('/accounts/invalid/')  
      
def  loggedin(request):
    context = RequestContext(request)
    return render_to_response('loggedin.html',context)
def  invalid_login(request):
    context = RequestContext(request)
    return render_to_response('invalid_login.html',context)

def  logout(request):
    auth.logout(request)
    context = RequestContext(request)
    return render_to_response('logout.html',context)


def register_user(request):
    form = MyRegistrarionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if form.cleaned_data['criarDisciplinasPadrao']:
            for disciplina in disciplinasPadrao:
                novaDisciplina = Disciplina()
                novaDisciplina.nome = disciplina['nome']
                novaDisciplina.label = disciplina['label']
                novaDisciplina.user = user
                novaDisciplina.save()
        return HttpResponseRedirect('/accounts/register_success')
    args  = {}
    args.update(csrf(request))
    args['form'] = form

    context = RequestContext(request, args)
    return render_to_response('register.html', context)  





def register_success(request):
    context = RequestContext(request)
    return render_to_response('register_success.html',context)

@login_required
def my_account(request):
    return HttpResponseRedirect('/accounts/get/%d' %request.user.id )

@login_required
def get(request, idObj = 1):
    context = RequestContext(request, {'account': User.objects.get(id = idObj)})
    return render_to_response('account/get.html',context)  

@login_required
def delete(request, idObj):
    account = User.objects.get(pk=idObj)
    if request.method == "POST":
        auth.logout(request)
        account
        account.delete()
        return HttpResponseRedirect('/')

    context = RequestContext(request, {'account': account})
    return render_to_response('account/delete.html', context)


@login_required
def update(request, idObj):
    account = User.objects.get(pk=idObj)
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/my_account/')
    else:
        form = MyUserChangeForm(instance=account)
    context = RequestContext(request, {'form': form, 'idObj': idObj})
    return render_to_response('account/update.html', context)    


@login_required
def change_password(request):
    form = PasswordChangeForm(data=request.POST or None, user = request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect('/accounts/my_account/')
    context = RequestContext(request, {'form': form})
    return render_to_response('account/change_password.html', context)    



