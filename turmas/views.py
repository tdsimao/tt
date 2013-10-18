#from  django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from  django.http import HttpResponseRedirect
#from  django.template.loader import  get_template
#from django.template import Context
from django.template import RequestContext

from django.shortcuts import render_to_response
#from django.views.generic.base import TemplateView

#from django.core.context_processors import csrf

from django.contrib.auth.decorators import login_required
from models import Turma 
from forms import TurmaForm
from grades.models import Grade
#from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404



@login_required
def list(request, idGrade):
    grade = Grade.objects.get(id = idGrade)
    grade.totalAulas = grade.dias * grade.auladia
    
    context = RequestContext(request, {'turmas': Turma.objects.all().filter(grade = grade),
                                       'grade' : grade})
    return render_to_response('turma/list.html',context)
    
@login_required
def get(request, idObj = 1):
    turma = Turma.objects.get(id = idObj)
    print turma.aula_set.all()
    grade = turma.grade
    context = RequestContext(request, {'turma': turma, 'grade':grade})
    return render_to_response('turma/get.html',context)  

@login_required
def create(request,idGrade):
    form = TurmaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        turma = form.save(commit=False)
        grade = Grade.objects.get(id = idGrade)
        turma.grade = grade
        turma.save()
        return HttpResponseRedirect('/aulas/create/%s' %turma.id)
        #return HttpResponseRedirect('/grades/get/%s' % idGrade)

    context = RequestContext(request, {'form': form, 'idGrade':idGrade})
    return render_to_response('turma/create.html', context)  


@login_required
def delete(request, idObj):
    turma = Turma.objects.get(pk=idObj)
    if request.method == "POST":
        turma.delete()
        return HttpResponseRedirect('/turmas/%s'%turma.grade.id)

    context = RequestContext(request, {'turma': turma})
    return render_to_response('turma/delete.html', context)


@login_required
def update(request, idObj):
    turma = Turma.objects.get(pk=idObj)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/turmas/%s'%turma.grade.id)
    else:
        form = TurmaForm(instance=turma)
    context = RequestContext(request, {'form': form, 'turma': turma})
    return render_to_response('turma/update.html', context)	

