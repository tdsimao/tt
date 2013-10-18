#from  django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from  django.http import HttpResponseRedirect
#from  django.template.loader import  get_template
#from django.template import Context
from django.template import RequestContext

from django.shortcuts import render_to_response
#from django.views.generic.base import TemplateView

#from django.core.context_processors import csrf

from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from models import Restricao 
from forms import RestricaoForm
from grades.models import Grade
from professores.models import Professor
from aulas.models import Aula
#from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404





@login_required
def update(request, idGrade, idProfessor):
    """
        Cria-se uma lista linhas de formularios,  um para cada restricao
        
    """
    dias_da_semana = ["SEG","TER","QUA","QUI","SEX","SAB","DOM"]
    
    
    grade = Grade.objects.get(pk=idGrade)
    professor = Professor.objects.get(pk=idProfessor)
    
    restricoes = Restricao.objects.filter(professor = professor,slot__in = grade.slot_set.all()).order_by('slot__horario')
    forms = []
          
    
    if request.method == 'POST':
        a = 0
        b = grade.dias
        for i in range(grade.auladia):
            forms.append([])
            for restricao in restricoes[a:b]:
                forms[i].append(RestricaoForm(request.POST, prefix=str(restricao.id), instance = restricao))
            a=b
            b=b+grade.dias        
                    
            
        formsValidos = True
        for row in forms:
            for form in row:
                if not form.is_valid():
                    formsValidos = False
        if formsValidos:
            for row in forms:
                for form in row:
                    form.save()
            
            return HttpResponseRedirect('/restricoes/list/%d' %grade.id)
            
        
    else:
        forms = []
        a = 0
        b = grade.dias
        for i in range(grade.auladia):
            forms.append([])
            for restricao in restricoes[a:b]:
                forms[i].append(RestricaoForm(prefix=str(restricao.id), instance = restricao))
            a=b
            b=b+grade.dias   
    
    dias_da_semana = dias_da_semana[0:grade.dias]
    context = RequestContext(request, {'forms': forms, 'idGrade': idGrade, 'idProfessor':idProfessor, 'dias_da_semana':dias_da_semana})
    return render_to_response('restricao/update.html', context)



def list(request, idGrade):
    dias_da_semana = ["SEG","TER","QUA","QUI","SEX","SAB","DOM"]
    tipos = ["Indisponivel","Indesejavel","Disponivel"]
    grade = Grade.objects.get(pk=idGrade)    
    professores = grade.getProfessores()
    
    dict_restricoes = {}
    
    #
    # Cria dicionario de restricoes, contendo uma tabela de restricoes para cada professor
    #
    for professor in professores:
        
        aux = Restricao.objects.filter(professor = professor,slot__in = grade.slot_set.all()).order_by('slot__horario')
        aux2 = []
        a = 0
        b = grade.dias
        for i in range(grade.auladia):
            aux2.append([])
            for r in aux[a:b]:
                #aux2[i].append(tipos[r.tipo]+str(r.slot))
                aux2[i].append(tipos[r.tipo])
            a=b
            b=b+grade.dias        
                    
        dict_restricoes[professor] = aux2
    dias_da_semana = dias_da_semana[0:grade.dias]
    context = RequestContext(request, {'grade': grade, 'dict_restricoes' : dict_restricoes, 'dias_da_semana': dias_da_semana,'menus':['restricoes']})
    return render_to_response('restricao/list.html', context)    

