#from  django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from  django.http import HttpResponseRedirect
#from  django.template.loader import  get_template
#from django.template import Context
from django.template import RequestContext

from django.shortcuts import render_to_response
#from django.views.generic.base import TemplateView

#from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from models import Grade 
from forms import GradeForm
#from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404

@login_required
def list(request):
    context = RequestContext(request, {'grades': Grade.objects.all().filter(user = request.user)})
    return render_to_response('grade/list.html',context)
    
    
@login_required
def get(request, idObj = 1):
    #return HttpResponseRedirect('/turmas/%s' % idObj)
    grade = Grade.objects.get(id = idObj)
    grade.totalAulas = grade.dias * grade.auladia
    grade.getProfessores()
    context = RequestContext(request, {'grade': grade,'menus':['turmas']})
    return render_to_response('grade/get.html',context)  
"""

def get(request, idObj = 1):
    return render_to_response('grade/get.html',
                              {'grade' : Grade.objects.get(id = idObj)})  
"""

@login_required
def create(request):
    form = GradeForm(request.POST or None)
    print (form.fields)
    if request.method == 'POST' and form.is_valid():
        grade = form.save(commit=False)
        grade.user = request.user
        grade.save()
        grade.setSlots()
        return HttpResponseRedirect('/grades/')

    context = RequestContext(request, {'form': form})
    return render_to_response('grade/create.html', context)  


@login_required
def delete(request, idObj):
    grade = Grade.objects.get(pk=idObj)
    if request.method == "POST":
        grade.delete()
        return HttpResponseRedirect('/grades/')

    context = RequestContext(request, {'grade': grade})
    return render_to_response('grade/delete.html', context)


@login_required
def update(request, idObj):
    grade = Grade.objects.get(pk=idObj)
    auladia = grade.auladia
    dias = grade.dias
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save()
            if (grade.dias != dias) or (grade.auladia != auladia):
                grade.setSlots()
                
            return HttpResponseRedirect('/grades/')
    else:
        form = GradeForm(instance=grade)
    context = RequestContext(request, {'form': form, 'idObj': idObj})
    return render_to_response('grade/update.html', context)	

def addTurma(request, idObj = 1):
    return HttpResponseRedirect('/turmas/create/%d',idObj)




            
    
