#from  django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from  django.http import HttpResponseRedirect
#from  django.template.loader import  get_template
#from django.template import Context
from django.template import RequestContext

from django.shortcuts import render_to_response
#from django.views.generic.base import TemplateView

#from django.core.context_processors import csrf

from django.contrib.auth.decorators import login_required
from models import Aula 
from forms import AulaForm
from turmas.models import Turma
from disciplinas.models import Disciplina
from restricoes.models import addRestricoesPadrao,Restricao
#from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404


"""
@login_required
def list(request):
    print  dir(Aula.objects.all().filter(user = request.user)[0])
    context = RequestContext(request, {'aulas': Aula.objects.all().filter(user = request.user)})
    return render_to_response('aula/list.html',context)
    
@login_required
def get(request, idObj = 1):
    context = RequestContext(request, {'aula': Aula.objects.get(id = idObj)})
    return render_to_response('aula/get.html',context)  

"""

@login_required
def create(request,turmaId):
    turma = Turma.objects.get(pk=turmaId)
    
    form = AulaForm(request.POST or None, usuario = request.user, turma = turma)
    
    if request.method == 'POST' and form.is_valid():
        aula = form.save(commit=False)
        aula.turma = turma
        aula.save()

        """
            Checa se professor ainda nao da aula para turma.grade
            nesse caso cadastrar restricoes do professor com valor padrao
            posteriormente pedir para usuario atualizar essas retricoes
        """
        
        #if aula.professor.getRestricoes(turma.grade) == []:
        #restricoes = Restricao.objects.filter(professor = aula.professor,slot__in = turma.grade.slot_set.all()).order_by('slot__horario').count
        
        if Restricao.objects.filter(professor = aula.professor,slot__in = turma.grade.slot_set.all()).order_by('slot__horario').count() == 0:
            addRestricoesPadrao(turma.grade,aula.professor)
        if turma.totalAulas() == turma.grade.dias * turma.grade.auladia:
            return HttpResponseRedirect('/grades/get/%s' %turma.grade.id)
        return HttpResponseRedirect('/aulas/create/%s' %turmaId)
    print form
    context = RequestContext(request, {'form': form, 'turma' : turma})
    return render_to_response('aula/create.html', context)  


@login_required
def delete(request, idObj):
    aula = Aula.objects.get(pk=idObj)
    if request.method == "POST":
        aula.delete()
        return HttpResponseRedirect('/grades/get/%s'% aula.turma.grade.id)

    context = RequestContext(request, {'aula': aula})
    return render_to_response('aula/delete.html', context)


@login_required
def update(request, idObj):
    aula = Aula.objects.get(pk=idObj)
    if request.method == 'POST':
        form = AulaForm(request.POST, instance=aula, usuario = request.user)
        if form.is_valid():
            form.save()
            turma = aula.turma

            if Restricao.objects.filter(professor = aula.professor,slot__in = turma.grade.slot_set.all()).order_by('slot__horario').count() == 0:
                addRestricoesPadrao(turma.grade,aula.professor)
            if turma.totalAulas() == turma.grade.dias * turma.grade.auladia:
                return HttpResponseRedirect('/grades/get/%s' %turma.grade.id)
            return HttpResponseRedirect('/aulas/create/%s' %turma.id)
    else:
        form = AulaForm(instance=aula, usuario = request.user)
    context = RequestContext(request, {'form': form, 'aula': aula})
    return render_to_response('aula/update.html', context)	





@login_required
def get_professor_set(request):
    print '-________________________________________________________-'
    print request.POST
    if request.method == 'POST':
        idDisciplina = request.POST['disciplina']
        
        print idDisciplina
    else:
        idDisciplina = ''
    professores = Disciplina.objects.get(id=idDisciplina).professor_set.all()
    context = RequestContext(request, {'professores': professores})
    return render_to_response('aula/get_professor_set.html', context)    

