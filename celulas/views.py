#from  django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from  django.http import HttpResponseRedirect
#from  django.template.loader import  get_template
#from django.template import Context
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.views.generic.base import TemplateView

#from django.core.context_processors import csrf

from django.contrib.auth.decorators import login_required
from models import Celula, Encontro
from forms import CreateCelulaForm
from grades.models import Grade
from src.variaveisGlobais import dias_da_semana
from algoritmos import algGenetico
#from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404



@login_required
def list(request, idGrade):
    grade = Grade.objects.get(id = idGrade)
    dias = dias_da_semana[0:grade.dias]
    turmas = grade.turma_set.all()
    slots = grade.slot_set.order_by('dia','horario').all()
    celulas = Celula.objects.filter(grade = grade)        
    horarios = {}
    #print 'request:',request.POST
    old_post = request.session.get('_old_post')
    form = CreateCelulaForm(old_post or None)
    if request.POST:
        form.is_valid()
    for celula in celulas:
        
        encontrosCelula = Encontro.objects.filter(celula = celula)
        horarios[celula] = {}
        for slot in slots:
            encontrosSlot = encontrosCelula.filter(slot=slot)
            horarios[celula][slot] = {}
            
            for turma in turmas:
                try:
                    encontro = encontrosSlot.get(celula = celula,slot=slot, aula__turma = turma)
                    #encontro = encontrosSlot.get(aula__turma = turma)
                except Encontro.DoesNotExist:
                    print 'Encontro.DoesNotExist'
                    encontro = None
                except Encontro.MultipleObjectsReturned:
                    encontro = encontrosSlot.filter(celula = celula,slot=slot, aula__turma = turma).all()[0]
                    print 'Encontro.MultipleObjectsReturned'
                horarios[celula][slot][turma] = encontro
    
    
    mensagens = request.session.get('mensagens',[])
    if mensagens != []:
        request.session.__delitem__('mensagens')
    
    context = RequestContext(request, {'menus':['horarios'],
                                       'grade' : grade,
                                       'dias_da_semana':dias,
                                       'turmas':turmas,
                                       'horarios':horarios,
                                       'form':form,
                                       'mensagens':mensagens,
                                       'slots':slots})
    return render_to_response('celula/list.html',context)
    
    
    
    
    
@login_required
def create(request,idGrade):
    grade = Grade.objects.get(id = idGrade)
    
    form = CreateCelulaForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        
        for i in range(form.cleaned_data['repeticoes']):
            algGenetico.criarHorario(grade = grade,opcoes = form.cleaned_data)
        
        
    request.session['_old_post'] = request.POST
    return HttpResponseRedirect('/celulas/list/%s' % idGrade)

    
@login_required
def delete(request, idObj):
    
    celula = Celula.objects.get(pk=idObj)
    if request.method == "POST":
        idGrade = celula.grade.id
        celula.delete()
        
        return HttpResponseRedirect('/celulas/list/%s' % idGrade)

    context = RequestContext(request, {'celula': celula})
    return render_to_response('celula/delete.html', context)


@login_required
def avaliar(request, idObj):
    celula = Celula.objects.get(pk=idObj)
    grade = celula.grade
    turmas,quantidadeTurmas,aulas,slots,tipoRestricaoProfessorNoSlot,minimoDiasProfessor = algGenetico.carregarDados(grade)
    
    celulaAlg = algGenetico.CelulaAlg(grade)
    for slot in slots:
        celulaAlg.encontros[slot] = {}
    for encontro in celula.encontro_set.all():
        celulaAlg.encontros[encontro.slot][encontro.aula.turma] = encontro
        
    
    
    mensagens = algGenetico.avaliacaoDetalhada(celulaAlg,grade,turmas,aulas,slots,tipoRestricaoProfessorNoSlot,minimoDiasProfessor)
    
        
    request.session['mensagens'] = mensagens
    return HttpResponseRedirect('/celulas/list/%s' % celula.grade.id)