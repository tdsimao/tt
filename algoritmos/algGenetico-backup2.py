# -*- coding: utf-8 -*- 
from celulas.models import Celula, Encontro
from random import choice, random, sample, randint
from time import time,strftime,localtime
from src.variaveisGlobais import pesos
from csv import DictWriter
from copy import deepcopy
from django.db import transaction


class CelulaAlg():
    
    #    classe criada para acumular lista de encontros sem salva-los
    #    e editar o metodo save() permitindo salvar os encontros
    
    
    
    
    def __init__(self, grade):
        #super(Celula,self).__init__(*args, **kwargs)
        self.encontros = {}
        self.grade = grade
        self.fitness = 0
        
    @transaction.commit_manually
    def save(self, *args, **kwargs):
        newCel = Celula()
        
        try:
        
            #newCel = Celula()
            newCel.grade = self.grade
            newCel.fitness = self.fitness
            
            if getattr(self, 'commit', True):
                # Caso seja necessario salvar
                newCel.save()
                # salva tambem todos os encontros
                for slot in self.encontros.values():
                    for encontro in slot.values():
                        encontro.celula = newCel
                        encontro.save()
        except: 
            transaction.rollback()
        else:
            transaction.commit() 

        return newCel
    
    def __str__(self):
        return str(self.fitness)+' '+str(self.grade) 
    
    def __unicode__(self):
        return str(self.fitness)+' '+str(self.grade) 
        

def avaliacao(celula,grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot):
    
    #=======================================================================
    # Verifica Criterios
    #     Número de choques de professores
    #     Número de aulas em horário inviável para algum professor
    #     Número de aulas em horário indesejável para algum professor
    #TODO Número de vezes que houve blocos de disciplinas
    #TODO Número de aulas que estão sendo ministradas desrespeitando o limite diário de aulas de uma mesma disciplina
    #     Número de janelas no horário dos professores
    #     Número de dias em excesso dos professores (diasProfessorVaiNaEscola - totalDiasProfessoṛ/grade.auladia)
    #TODO Número de aulas isoladas no horário dos professores
    # 
    #
    #    Gera o Fitness da solucao.
    #=======================================================================
    
    #Penalidades
    choqueProfessores = 0
    professorInviavel = 0
    professorIndesejavel = 0
    janelas = 0
    professoresComExcessoDias  = 0
    
    
    #professores = totalAulasProfessor.keys()
    totalDiasProfessor = {}
    
    
    #encontros = celula.encontros
    for dia in range(grade.dias):
        ultimaAula = {}
        professoresNoDia = []
        for horario in range(grade.auladia):
            slot = slots[dia*grade.dias+horario]
            professoresNoSlot = []
            
            for encontro in celula.encontros[slot].values():
                professor = encontro.aula.professor
                #
                # VERIFICA SE O PROFESSOR DA MAIS DE UMA AULA NO SLOT
                #
                if professor in professoresNoSlot:
                    choqueProfessores = choqueProfessores + 1
                else:
                    professoresNoSlot.append(professor)
                #
                # VERFICA A DISPONIBILIDADE DO PROFESSOR NO HORARIO
                #
                if  tipoRestricaoProfessorNoSlot[professor][slot]  == 0:
                    professorInviavel = professorInviavel + 1
                elif tipoRestricaoProfessorNoSlot[professor][slot]  == 1:
                    professorIndesejavel = professorIndesejavel + 1
                
                if ultimaAula.get(professor) == 'Janela':
                    janelas = janelas + 1
                ultimaAula[professor] = encontro.aula
                
            for professor in ultimaAula.keys():
                if not professor in professoresNoSlot:
                    ultimaAula[professor] = 'Janela'
            professoresNoDia = list(set(professoresNoDia + professoresNoSlot))
        for professor in professoresNoDia:
            totalDiasProfessor[professor] = totalDiasProfessor.get(professor,0) + 1
            
            
    for professor,quantidadeAulas in totalAulasProfessor.items(): 
        professoresComExcessoDias += (totalDiasProfessor[professor] - quantidadeAulas/grade.auladia)
    totalPenalidades = pesos['choqueProfessores'] * choqueProfessores + pesos['professorInviavel'] * professorInviavel + pesos['professorIndesejavel'] * professorIndesejavel + pesos['janelas'] * janelas + pesos['professoresComExcessoDias'] * professoresComExcessoDias
    
    
    celula.fitness = (1./(100.+totalPenalidades))*100
    


def avaliacaoDetalhada(celula,grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot):
    
    #=======================================================================
    # Verifica Criterios
    #     Número de choques de professores
    #     Número de aulas em horário inviável para algum professor
    #     Número de aulas em horário indesejável para algum professor
    #TODO Número de vezes que houve blocos de disciplinas
    #TODO Número de aulas que estão sendo ministradas desrespeitando o limite diário de aulas de uma mesma disciplina
    #     Número de janelas no horário dos professores
    #     Número de dias em excesso dos professores (diasProfessorVaiNaEscola - totalDiasProfessoṛ/grade.auladia)
    #TODO Número de aulas isoladas no horário dos professores
    # 
    #
    #    Gera o Fitness da solucao.
    #=======================================================================
    
    #Penalidades
    choqueProfessores = 0
    professorInviavel = 0
    professorIndesejavel = 0
    janelas = 0
    professoresComExcessoDias  = 0
    excessoAulasNoMesmoDia = 0
    
    
    professores = totalAulasProfessor.keys()
    totalDiasProfessor = {}
    mensagens = []
    encontros = celula.encontros
    for dia in range(grade.dias):
        ultimaAula = {}
        professoresNoDia = []
        
        professoresNoDiacomATurma = {}
        
        for horario in range(grade.auladia):
            slot = slots[dia*grade.dias+horario]
            professoresNoSlot = []
            
            for encontro in celula.encontros[slot].values():
                professor = encontro.aula.professor
                #
                # VERIFICA SE O PROFESSOR DA MAIS DE UMA AULA NO SLOT
                #
                if professor in professoresNoSlot:
                    mensagens.append('[choqueProfessores]\t'+str(slot)+'\t'+str(professor))
                    choqueProfessores = choqueProfessores + 1
                else:
                    professoresNoSlot.append(professor)
                #
                # VERFICA A DISPONIBILIDADE DO PROFESSOR NO HORARIO
                #
                if  tipoRestricaoProfessorNoSlot[professor][slot]  == 0:
                    mensagens.append('[professorInviavel]\t'+str(slot)+'\t'+str(professor))
                    professorInviavel = professorInviavel + 1
                elif tipoRestricaoProfessorNoSlot[professor][slot]  == 1:
                    mensagens.append('[professorIndesejavel]\t'+str(slot)+'\t'+str(professor))
                    professorIndesejavel = professorIndesejavel + 1
                
                
                #
                # VERFICA SE OCORREU JANELA
                #  isto é,  se o professor ja deu uma aula no dia depois teve uma horario vago
                #              e agora tem uma nova aula no mesmo dia
                #
                if ultimaAula.get(professor) == 'Janela':
                    mensagens.append('[janela]\t'+str(slot)+'\t'+str(professor))
                    janelas = janelas + 1
                ultimaAula[professor] = encontro.aula
                
                
                #
                # Contabiliza total de aulas entre professor e turma em um mesmo dia
                #
                
                professoresNoDiacomATurma[professor] =  professoresNoDiacomATurma.get(professor,{})
                professoresNoDiacomATurma[professor][encontro.aula.turma] = professoresNoDiacomATurma[professor].get(encontro.aula.turma,0)+1
            
                
                    
                    
            for professor in ultimaAula.keys():
                if not professor in professoresNoSlot:
                    ultimaAula[professor] = 'Janela'
            professoresNoDia = list(set(professoresNoDia + professoresNoSlot))
            
            
            
        for professor,quantidadeAulasTurma in professoresNoDiacomATurma.iteritems():
            for turma,quantidadeAulas in quantidadeAulasTurma.iteritems():
                if quantidadeAulas > 2:
                    excessoAulasNoMesmoDia = excessoAulasNoMesmoDia + (quantidadeAulas - 2)
                    mensagens.append('[excessoAulasNoMesmoDia]\t'+str(professor)+' '+str(turma)+' - dia '+str(dia))
                    
        for professor in professoresNoDia:
            totalDiasProfessor[professor] = totalDiasProfessor.get(professor,0) + 1
            
            
    for professor,quantidadeAulas in totalAulasProfessor.items(): 
        mensagens.append('professoresComExcessoDias\t '+str(professor)+': '+str(totalDiasProfessor[professor])+' dias')
        professoresComExcessoDias += (totalDiasProfessor[professor] - quantidadeAulas/grade.auladia)
        
    mensagens.append('choqueProfessores = '+str(choqueProfessores ))
    mensagens.append('professorInviavel = '+str( professorInviavel ))
    mensagens.append('professorIndesejavel = '+str( professorIndesejavel ))
    mensagens.append('janelas = '+str( janelas ))
    mensagens.append('professoresComExcessoDias = '+str( professoresComExcessoDias))
    totalPenalidades = 0
    totalPenalidades += pesos['choqueProfessores'] * choqueProfessores
    totalPenalidades += pesos['professorInviavel'] * professorInviavel
    totalPenalidades += pesos['professorIndesejavel'] * professorIndesejavel
    totalPenalidades += pesos['janelas'] * janelas
    totalPenalidades += pesos['professoresComExcessoDias'] * professoresComExcessoDias
    totalPenalidades += pesos['excessoAulasNoMesmoDia'] * excessoAulasNoMesmoDia
    print totalPenalidades
    
    print  'penalidade\t',1./(1.+totalPenalidades)
    print  'penalidade2\t',(1./(100.+totalPenalidades))*100
    celula.fitness = (1./(100.+totalPenalidades))*100
    return mensagens
    



def criarCelula(grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot,opcoes):
    
    # cria uma celula que representa uma solucao para a grade
    # possui um conjunto de encontros
    # encontros sao definidos aleatoriamente
    celula = CelulaAlg(grade)
    for slot in slots:
        celula.encontros[slot] = {}
    
    # cria encontros definindo um slotsVazio da turma para cada aula
    aulasNaoAtribuidas = {}
    for turma in turmas:
        aulasNaoAtribuidas[turma] = []
        for aula in aulas[turma]:
            for i in range(aula.quantidade):
                aulasNaoAtribuidas[turma].append(aula)
        for slot in slots:
            
            """
            Em vez de checar se as aulas acabarem checar se a grade é valida
            """
            
            aula = choice(aulasNaoAtribuidas[turma])
            aulasNaoAtribuidas[turma].remove(aula)
            encontro = Encontro()
            encontro.slot = slot
            encontro.aula = aula
            celula.encontros[slot][turma] = encontro
        
    return celula
    


def fimDoAlgoritmo(populacao,opcoes):
    if populacao['geracao'] == opcoes['limiteGeracoes']:
        print 'Limite de Gerações Atingido'
        return True
    if populacao['melhorIndividuo'].fitness == 1:
        print 'Solução ótima encontrada'
        return True
    tempoLimite = opcoes['limiteTempo'] * 60 * 360 #transforma limite de tempo de hora para segundos
    if time() - populacao['tempoInicial']  > tempoLimite:
        print 'Tempo Esgotado'
        return True
        
    return False
    


def  selecao(populacao,opcoes):
    pais = []
    
    quantidadePais = (opcoes['populacao'] * opcoes['quantidadePais']) / 100
    
    
    # ROLETA
    
    if  opcoes['metodoSelecao'] == 'roleta':
        
        
        fitnessTotal  = populacao['fitnessTotal']
        """
        for celula in populacao['individuos']:
            fitnessTotal = fitnessTotal + celula.fitness
          """  
        concorrentes = populacao['individuos']
        while len(pais) < quantidadePais:
            somaFitness = 0
            t = random() * fitnessTotal
            for celula in populacao['individuos']:
                somaFitness = somaFitness + celula.fitness
                #print 'soma',somaFitness
                if somaFitness > t:
                    pais.append(celula)
                    fitnessTotal -= celula.fitness
                    concorrentes.remove(celula)
                    
                    break
                
    elif  opcoes['metodoSelecao'] == 'torneio':
        concorrentes = populacao['individuos']
        while len(pais) < quantidadePais:
            concorrente1 = choice(concorrentes)
            concorrente2 = choice(concorrentes)
            if concorrente1.fitness > concorrente2.fitness:
                pais.append(concorrente1)
                concorrentes.remove(concorrente1)
            else:
                pais.append(concorrente2)
                concorrentes.remove(concorrente2)
            
        """
        concorrentes = sample(populacao['individuos'],quantidadePais*2)
        while concorrentes != []:
            concorrente1 = choice(concorrentes)
            concorrentes.remove(concorrente1)
            concorrente2 = choice(concorrentes)
            concorrentes.remove(concorrente2)
            if concorrente1.fitness>concorrente2.fitness:
                pais.append(concorrente1)
            else:
                pais.append(concorrente2)
            """
    elif  opcoes['metodoSelecao'] == 'aleatorio':
        pais = sample(populacao['individuos'],quantidadePais)
        for individuo in pais:
            populacao['individuos'].remove(individuo)
        
    else:
        print 'MÉTODO DE SELEÇÃO INVÁLIDO'
        
    """ 
    for individuo in pais:
        populacao['individuos'].remove(individuo)
        """
    return pais
    


def showEncontros(encontros):
    print '_'*50
    print '\t\t',
    for turma in encontros.values()[0]:
        print turma , '\t',
    print '\n'
    print '_'*50
    for slot, turmas in encontros.items():
        print slot.dia,'\t',slot.horario,'\t',
        for encontro in turmas.values():
            print encontro.aula.professor.label,
        print '\n'
    print ''
            
        


def crossover(pais,opcoes,quantidadeTurmas,grade):
    filhos = []
    if  opcoes['metodoCrossover'] == '1px':
        while pais != []:
            #escolhe ponto de cruzamento
            pontoCruzamento = randint(1,quantidadeTurmas-1)
            pai1 = choice(pais)
            pais.remove(pai1)
            pai2 = choice(pais)
            pais.remove(pai2)
            
            """
            print 'pontoCruzamento', pontoCruzamento
            print pai1,pai1.encontros
            showEncontros(pai1.encontros)
            print pai2,pai2.encontros
            showEncontros(pai2.encontros)
            """
            
            filho1 = CelulaAlg(grade)
            filho2 = CelulaAlg(grade)
            slots = pai1.encontros.keys()
            for slot in slots:
                filho1.encontros[slot] = dict(pai1.encontros[slot].items()[0:pontoCruzamento] + pai2.encontros[slot].items()[pontoCruzamento:]) 
                filho2.encontros[slot] = dict(pai2.encontros[slot].items()[0:pontoCruzamento] + pai1.encontros[slot].items()[pontoCruzamento:]) 
            
            """
            showEncontros(filho1.encontros)
            showEncontros(filho2.encontros)
            """
            
            
            filhos.append(filho1)
            filhos.append(filho2)
    else:
        print 'Método de cruzamento inválido'
                    
    return filhos
    



def mutacao(individuos,opcoes):
    probabilidadeMutacao = float(opcoes['probabilidadeMutacao'])/1000
    for celula in individuos:
        if  random() < probabilidadeMutacao:
            """
            Sorteia 2 slots 
            sorteia um encontro do primeiro slot
            a seguir seleciona o encontro do segundo slot cuja aula é compatível com a turma do encontro selecionado
            
            """
            
            slot1,slot2 = sample(celula.encontros.values(),2)
            encontroA = choice(slot1.values())
            encontroB = slot2[encontroA.aula.turma]
                    
            #troca as aulas dos encontros selecionados
            aulaAux = encontroA.aula
            encontroA.aula = encontroB.aula
            encontroB.aula = aulaAux
    




def salvarProgresso(populacao,arquivoSaida,opcoes):
    status = {}
    tamanhoPopulacao = len(populacao['individuos'])
    status['geracao'] = populacao['geracao'] 
    status['melhorFitness'] = populacao['melhorIndividuo'].fitness
    status['fitnessMedio'] = populacao['fitnessTotal']/tamanhoPopulacao
    status['tamanhoPopulacao'] = float(tamanhoPopulacao)/opcoes['populacao']
    
    for (key,value) in status.items():
        print key,':',value, '\t|',
    print ''
    #f = open(str(grade)+str(grade.id)+'.csv','a')
    f = open(arquivoSaida,'a')
    writer = DictWriter(f,['geracao','melhorFitness','fitnessMedio','tamanhoPopulacao'])
    writer.writerow(status)
    f.close()

def iniciarControladorProgresso(arquivoSaida):
    #inicia arquivo de saida
    # criando cabeçalho
    status = {}
    status['geracao'] = 'geracao'
    status['melhorFitness'] = 'melhorFitness'
    status['fitnessMedio'] = 'fitnessMedio'
    status['tamanhoPopulacao'] = 'tamanhoPopulacao'
    #f = open(str(grade)+str(grade.id)+'.csv','w')
    f = open(arquivoSaida,'w')
    #writer = DictWriter(f,status.keys())
    writer = DictWriter(f,['geracao','melhorFitness','fitnessMedio','tamanhoPopulacao'])
    writer.writerow(status)
    f.close()
    


def carregarDados(grade):
    """
        BUSCA TODAS AS INFORMAÇÕES DO BANCO DE DADOS REFERENTE A GRADE
    
    """
    turmas = grade.turma_set.all()
    quantidadeTurmas = len(turmas)
    aulas = {}
    totalAulasProfessor = {}
    for turma in turmas:
        aulas[turma] = turma.aula_set.all()
        for aula in turma.aula_set.all():
            totalAulasProfessor[aula.professor] = totalAulasProfessor.get(aula.professor,0) + aula.quantidade
            
    #for p,quantidade in totalAulasProfessor.items():
    #    print p,quantidade
    
    slots = grade.slot_set.order_by('dia','horario').all()
    
    #import pprint
    #pprint.pprint(locals())
    
    
    tipoRestricaoProfessorNoSlot  = {}
    for professor in totalAulasProfessor.keys():
        tipoRestricaoProfessorNoSlot[professor] = {}
        for slot in slots:
            tipoRestricaoProfessorNoSlot[professor][slot] = professor.restricao_set.get(slot=slot).tipo 
    return turmas,quantidadeTurmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot
    


def populacaoInicial(grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot,opcoes):
    #POPULACAO INICIAL
    populacao = {}
    populacao['individuos'] = []
    for i in range(opcoes['populacao']):
        celula = criarCelula(grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot,opcoes)
        populacao['individuos'].append(celula)
        
    populacao['geracao'] = 0
    return populacao    
    



def criarHorario(grade, opcoes):
    
    #  CHECAR SE A GRADE E VALIDA
    if not(grade.is_valid()):
        print 'Grade Invalida'
        return
    
    # checa se quantidade de individuos da seleção será par
    if ((opcoes['populacao'] * opcoes['quantidadePais']) / 100) % 2 != 0:
        opcoes['quantidadePais'] -=1
        print 'Ajustando quantidade de individuos da seleção para ',opcoes['quantidadePais'],'%'
    
    turmas,quantidadeTurmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot = carregarDados(grade)
    
    #POPULACAO INICIAL
    populacao = populacaoInicial(grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot,opcoes)
        
    for celula in populacao['individuos']:
        avaliacao(celula,grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot)
        
    melhorIndividuo = populacao['individuos'][0]
    
    
    populacao['melhorIndividuo'] = populacao['individuos'][0]
    populacao['fitnessTotal'] = 0
    populacao['tempoInicial'] = time()
    
    
    #localTime = localTime()
    data = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    print data
    arquivoSaida = 'saida/grade-'+str(grade.id)+'_'+data+'.csv'
    iniciarControladorProgresso(arquivoSaida)
    #ENQUANTO  CRITERIOS DE PARADA NÃO FOREM SATISFEITOS REPETE-SE AS AÇÕES
    while not(fimDoAlgoritmo(populacao,opcoes)):
        populacao['fitnessTotal'] = 0
        populacao['melhorIndividuo'] = populacao['individuos'][0]
        for celula in populacao['individuos']:
            populacao['fitnessTotal'] += celula.fitness
            if celula.fitness > populacao['melhorIndividuo'].fitness:
                populacao['melhorIndividuo'] = celula
                
        # se o melhor individuo da populacao for melhor que o melhor individuo ja encontrado
        # substitui o melhor individuo ja encontrado
        if populacao['melhorIndividuo'].fitness > melhorIndividuo.fitness:
            melhorIndividuo  = populacao['melhorIndividuo']
            
        
        
        #seleciona pais para cruzamento removendo-os do conjunto de individuos
        pais = selecao(populacao, opcoes)
        
        filhos = crossover(deepcopy(pais), opcoes, quantidadeTurmas,grade)
        
        mutacao(filhos, opcoes)
        
        #avalia filhos gerados
        for celula in filhos:
            avaliacao(celula,grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot)
            
        
        #
        # ATUALIZA CONJUNTO DE INDIVÍDUOS DA POPULAÇÃO
        
        s = random()
        print s * 100
        if s*100 < opcoes['chanceSobrevivencia']: 
            #SIMPLESMENTE SUBSTITUI OS PAIS PELOS FILHOS
            populacao['individuos'] += filhos
        else:
            #SELECIONA OS MELHORES ENTRE PAIS E FILHOS
            candidatos = pais + filhos
            candidatos = sorted(candidatos, key=lambda c: c.fitness)[::-1]
            populacao['individuos'] += candidatos[0:len(pais)]
        
        
        
        salvarProgresso(populacao,arquivoSaida,opcoes)
        
        populacao['geracao'] += 1
        
        
    print 'tempo final: ', time() - populacao['tempoInicial']
    #print 'Tempo para avaliar populacao de tamanho',opcoes['populacao'],': ',time()-inicio
    #inicio = time()
    
    melhorIndividuo.save()
    

    arquivoSaida = open('saida/grade-'+str(grade.id)+'_'+data+'.txt','w')
    arquivoSaida.write(str(opcoes))
    arquivoSaida.close()

