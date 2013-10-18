#from  django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from  django.http import HttpResponseRedirect
#from  django.template.loader import  get_template
#from django.template import Context
from django.template import RequestContext

from django.shortcuts import render_to_response
#from django.views.generic.base import TemplateView

#from django.core.context_processors import csrf

from django.contrib.auth.decorators import login_required
from models import Professor 
from forms import ProfessorForm
#from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404



@login_required
def list(request):
    context = RequestContext(request, {'professores': Professor.objects.filter(user = request.user).order_by('nome').all()})
    return render_to_response('professor/list.html',context)
    
@login_required
def get(request, idObj = 1):
    context = RequestContext(request, {'professor': Professor.objects.get(id = idObj)})
    return render_to_response('professor/get.html',context)  
"""

def get(request, idObj = 1):
    return render_to_response('professor/get.html',
                              {'professor' : Professor.objects.get(id = idObj)})  
"""

@login_required
def create(request):
    """
     importante passar user  para ProfessorForm
     pois define a lista de disciplinas possiveis 
     para o professor que esta sendo criado
    """
    form = ProfessorForm(request.POST or None, usuario = request.user)
    if request.method == 'POST' and form.is_valid():
        professor = form.save(commit=False)
        professor.user = request.user
        professor.save()
        form.save()
        return HttpResponseRedirect('/professores/')
    #form.disciplinas.choices = Disciplina.objects.all().filter(user = request.user)
    context = RequestContext(request, {'form': form})
    return render_to_response('professor/create.html', context)  


@login_required
def delete(request, idObj):
    professor = Professor.objects.get(pk=idObj)
    if request.method == "POST":
        professor.delete()
        return HttpResponseRedirect('/professores/')

    context = RequestContext(request, {'professor': professor})
    return render_to_response('professor/delete.html', context)


@login_required
def update(request, idObj):
    professor = Professor.objects.get(pk=idObj)
    form = ProfessorForm(request.POST or None, usuario = request.user, instance = professor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect('/professores/')
    context = RequestContext(request, {'form': form, 'idObj': idObj})
    return render_to_response('professor/update.html', context)	

