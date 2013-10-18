#from  django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from  django.http import HttpResponseRedirect
#from  django.template.loader import  get_template
#from django.template import Context
from django.template import RequestContext

from django.shortcuts import render_to_response
#from django.views.generic.base import TemplateView

#from django.core.context_processors import csrf

from django.contrib.auth.decorators import login_required
from models import Disciplina 
from forms import DisciplinaForm
#from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404



@login_required
def list(request):
    disciplinas = Disciplina.objects.filter(user = request.user).order_by('nome').all()
    context = RequestContext(request, {'disciplinas': disciplinas})
    return render_to_response('disciplina/list.html',context)
    
@login_required
def get(request, idObj = 1):
    context = RequestContext(request, {'disciplina': Disciplina.objects.get(id = idObj)})
    return render_to_response('disciplina/get.html',context)  
"""

def get(request, idObj = 1):
    return render_to_response('disciplina/get.html',
                              {'disciplina' : Disciplina.objects.get(id = idObj)})  
"""

@login_required
def create(request):
    form = DisciplinaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        disciplina = form.save(commit=False)
        disciplina.user = request.user
        disciplina.save()
        return HttpResponseRedirect('/disciplinas/')

    context = RequestContext(request, {'form': form})
    return render_to_response('disciplina/create.html', context)  


@login_required
def delete(request, idObj):
    disciplina = Disciplina.objects.get(pk=idObj)
    if request.method == "POST":
        disciplina.delete()
        return HttpResponseRedirect('/disciplinas/')

    context = RequestContext(request, {'disciplina': disciplina})
    return render_to_response('disciplina/delete.html', context)


@login_required
def update(request, idObj):
    disciplina = Disciplina.objects.get(pk=idObj)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina, usuario=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/disciplinas/')
    else:
        form = DisciplinaForm(instance=disciplina, usuario=request.user)
    context = RequestContext(request, {'form': form, 'idObj': idObj})
    return render_to_response('disciplina/update.html', context)	

