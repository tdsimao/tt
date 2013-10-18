# -*- coding: utf-8 -*- 
from celulas.models import Celula, Encontro
from random import choice, random, sample, randint,shuffle
from time import time,strftime,localtime
from src.variaveisGlobais import pesos,maxAulasPorDia
from csv import DictWriter,DictReader
from copy import deepcopy
from django.db import transaction
import os
import math

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
        


def avaliacao(celula,grade,turmas,aulas,slots,tipoRestricaoProfessorNoSlot,minimoDiasProfessor):
    
    #=======================================================================
    # Verifica Criterios
    #     Número de choques de professores
    #     Número de aulas em horário inviável para algum professor
    #     Número de aulas em horário indesejável para algum professor
    #TODO Número de vezes que houve blocos de disciplinas
    #     Número de aulas que estão sendo ministradas desrespeitando o limite diário de aulas de uma mesma disciplina
    #     Número de janelas no horário dos professores
    #     Número de dias em excesso dos professores (diasProfessorVaiNaEscola - totalDiasProfessoṛ/grade.auladia)
    #TODO Número de aulas isoladas no horário dos professores
    # 
    #
    #    Gera o Fitness da solucao.
    #=======================================================================
    
    #Penalidades
    penalidades = {}
    
    penalidades['choqueProfessores'] = 0
    penalidades['professorInviavel'] = 0
    penalidades['professorIndesejavel'] = 0
    penalidades['janelas'] = 0
    penalidades['professoresComExcessoDias']  = 0
    penalidades['excessoAulasNoMesmoDia']  = 0
    
    
    professores = minimoDiasProfessor.keys()
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
                    penalidades['choqueProfessores'] += 1
                else:
                    professoresNoSlot.append(professor)
                #
                # VERFICA A DISPONIBILIDADE DO PROFESSOR NO HORARIO
                #
                if  tipoRestricaoProfessorNoSlot[professor][slot]  == 0:
                    penalidades['professorInviavel'] += 1
                elif tipoRestricaoProfessorNoSlot[professor][slot]  == 1:
                    penalidades['professorIndesejavel'] += 1
                
                
                #
                # VERFICA SE OCORREU JANELA
                #  isto é,  se o professor ja deu uma aula no dia depois teve uma horario vago
                #              e agora tem uma nova aula no mesmo dia

                # ultimaAula armazena a quantos slots o professor ministrou sua ultima aula
                #
                if ultimaAula.get(professor,0) > 0:
                    penalidades['janelas'] += ultimaAula.get(professor)
                    #print '[janela]\tslot: '+str(slot)+'\tprofessor: '+str(professor)+"\ttamanho: "+str(ultimaAula.get(professor))
                ultimaAula[professor] = 0
                
                
                #
                # Contabiliza total de aulas entre professor e turma em um mesmo dia
                #
                
                professoresNoDiacomATurma[professor] =  professoresNoDiacomATurma.get(professor,{})
                professoresNoDiacomATurma[professor][encontro.aula.turma] = professoresNoDiacomATurma[professor].get(encontro.aula.turma,0)+1
            
                
                    
                    
            for professor in ultimaAula.keys():
                if not professor in professoresNoSlot:
                    ultimaAula[professor] += 1
            professoresNoDia = list(set(professoresNoDia + professoresNoSlot))
            
            
            
        for professor,quantidadeAulasTurma in professoresNoDiacomATurma.iteritems():
            for turma,quantidadeAulas in quantidadeAulasTurma.iteritems():
                if quantidadeAulas > 2:
                    penalidades['excessoAulasNoMesmoDia'] += (quantidadeAulas - 2)
                    #penalidades['excessoAulasNoMesmoDia'] += (quantidadeAulas - professor.maxAulasPorDiaPorTurma)
                    
        for professor in professoresNoDia:
            totalDiasProfessor[professor] = totalDiasProfessor.get(professor,0) + 1
            
            
    for professor,quantidadeAulas in minimoDiasProfessor.items(): 
        excesso = (totalDiasProfessor[professor] - quantidadeAulas)
        if excesso > 0:
            penalidades['professoresComExcessoDias']  += excesso
            
        
        
    totalPenalidades = 0
    #
    # Pondera total de penalidade segundo respectivos pesos
    #
    totalPenalidades += pesos['choqueProfessores'] * penalidades['choqueProfessores']
    totalPenalidades += pesos['professorInviavel'] * penalidades['professorInviavel']
    totalPenalidades += pesos['professorIndesejavel'] * penalidades['professorIndesejavel']
    totalPenalidades += pesos['janelas'] * penalidades['janelas']
    totalPenalidades += pesos['professoresComExcessoDias'] * penalidades['professoresComExcessoDias']
    totalPenalidades += pesos['excessoAulasNoMesmoDia'] * penalidades['excessoAulasNoMesmoDia']
    
    print totalPenalidades,penalidades
    
    celula.fitness = (1./(100.+totalPenalidades))*100
    return mensagens
    


def avaliacaoDetalhada(celula,grade,turmas,aulas,slots,tipoRestricaoProfessorNoSlot,minimoDiasProfessor):
    
    #=======================================================================
    # Verifica Criterios
    #     Número de choques de professores
    #     Número de aulas em horário inviável para algum professor
    #     Número de aulas em horário indesejável para algum professor
    #TODO Número de vezes que houve blocos de disciplinas
    #     Número de aulas que estão sendo ministradas desrespeitando o limite diário de aulas de uma mesma disciplina
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
    
    
    professores = minimoDiasProfessor.keys()
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
                    print professor
                    print tipoRestricaoProfessorNoSlot[professor]
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
            
            
    
            
    for professor,quantidadeAulas in minimoDiasProfessor.items(): 
        excesso = (totalDiasProfessor[professor] - quantidadeAulas)
        if excesso > 0:
            print professor,excesso
            mensagens.append('professoresComExcessoDias\t '+str(professor)+': '+str(excesso)+' dias em excesso')
            professoresComExcessoDias += excesso
            
        
        
    mensagens.append('choqueProfessores = '+str(choqueProfessores))
    mensagens.append('professorInviavel = '+str(professorInviavel))
    mensagens.append('professorIndesejavel = '+str(professorIndesejavel ))
    mensagens.append('janelas = '+str(janelas))
    mensagens.append('professoresComExcessoDias = '+str(professoresComExcessoDias))
    totalPenalidades = 0
    #
    # Pondera total de penalidade segundo respectivos pesos
    #
    totalPenalidades += pesos['choqueProfessores'] * choqueProfessores
    totalPenalidades += pesos['professorInviavel'] * professorInviavel
    totalPenalidades += pesos['professorIndesejavel'] * professorIndesejavel
    totalPenalidades += pesos['janelas'] * janelas
    totalPenalidades += pesos['professoresComExcessoDias'] * professoresComExcessoDias
    totalPenalidades += pesos['excessoAulasNoMesmoDia'] * excessoAulasNoMesmoDia
    
    print  'penalidade\t',1./(1.+totalPenalidades)
    print  'penalidade2\t',(1./(100.+totalPenalidades))*100
    celula.fitness = (1./(100.+totalPenalidades))*100
    return mensagens
    



def criarCelula(grade,turmas,aulas,slots,tipoRestricaoProfessorNoSlot,opcoes):
    
    # cria uma celula que representa uma solucao para a grade
    # possui um conjunto de encontros
    # encontros sao definidos aleatoriamente
    celula = CelulaAlg(grade)
    for slot in slots:
        celula.encontros[slot] = {}
    
    # cria encontros definindo para cada slot uma aulaNaoAtribuida
    aulasNaoAtribuidas = {}
    for turma in turmas:
        aulasNaoAtribuidas[turma] = []
        for aula in aulas[turma]:
            for i in range(aula.quantidade):
                aulasNaoAtribuidas[turma].append(aula)
        for slot in slots:
            
            aula = choice(aulasNaoAtribuidas[turma])
            
            #
            #  Heuristica:
            #           tenta alocar um professor disponivel no slot
            #
            numSorteios = 0
            while ((tipoRestricaoProfessorNoSlot[aula.professor][slot]  != 2) and (numSorteios < 10) ):
                aula = choice(aulasNaoAtribuidas[turma])
                numSorteios += 1
            
            
            
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
        sair = raw_input('Deseja  mesmo encerrar (0/1):')
        sair = (sair == '1' or sair == 's' or sair == 'S')
        if not sair:
            geracoesAcrescimo = input('Digite o numero de gerações de acrescimo:')
            opcoes['limiteGeracoes'] += geracoesAcrescimo
        return sair
        
    if populacao['melhorIndividuo'].fitness == 1:
        print 'Solução ótima encontrada'
        return True
        
        
    tempoLimite = opcoes['limiteTempo'] * 3600 #transforma limite de tempo de hora para segundos
    if time() - populacao['tempoInicial']  > tempoLimite:
        print 'Tempo Esgotado'
        return True
        sair = raw_input('Deseja  mesmo encerrar (0/1):')
        sair = (sair == '1' or sair == 's' or sair == 'S')
        if not sair:
            tempoAcrescimo = input('Digite o tempo de acrescimo (horas):')
            opcoes['limiteTempo'] += tempoAcrescimo
        return sair
        
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
    


def showEncontros(encontros,diretorioSaida):
    
    aux = 'Dia\tHora\t'
    for turma in encontros.values()[0]:
        aux += str(turma) + '\t'
    aux += '\n'
    for slot, turmas in encontros.items():
        aux += str(slot.dia)+'\t'+str(slot.horario)+'\t'
        for encontro in turmas.values():
            aux += encontro.aula.professor.label[0:6]+' / '+encontro.aula.disciplina.label[0:6]+'\t'
        aux += '\n'
    aux += '\n'
            
    f = open(os.path.join(diretorioSaida, 'horario.csv'),'w')
    f.write(aux)
    f.close()
        
            
            
        


def crossover(pais,opcoes,quantidadeTurmas,grade,turmas,diretorioSaida):
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
            #print pai1,pai1.encontros
            showEncontros(pai1.encontros,diretorioSaida)
            #print pai2,pai2.encontros
            showEncontros(pai2.encontros)
            """
            
            filho1 = CelulaAlg(grade)
            filho2 = CelulaAlg(grade)
            slots = pai1.encontros.keys()
            
            
            
            """
            #Versão 1 CROSSOVER 1px
            for slot in slots:
                filho1.encontros[slot] = dict(pai1.encontros[slot].items()[0:pontoCruzamento] + pai2.encontros[slot].items()[pontoCruzamento:]) 
                filho2.encontros[slot] = dict(pai2.encontros[slot].items()[0:pontoCruzamento] + pai1.encontros[slot].items()[pontoCruzamento:]) 
            """
            
            #Versão 2 CROSSOVER 1px
            for slot in slots:
                encontrosPai1 = pai1.encontros[slot].items()
                encontrosPai2 = pai2.encontros[slot].items()
                filho1.encontros[slot] = dict(encontrosPai1[0:pontoCruzamento] + encontrosPai2[pontoCruzamento:]) 
                filho2.encontros[slot] = dict(encontrosPai2[0:pontoCruzamento] + encontrosPai1[pontoCruzamento:]) 
            
            
            """
            #Versão 3 CROSSOVER 1px
            t1 = turmas[0:pontoCruzamento]
            t2 = turmas[pontoCruzamento:]
            
            
            for slot in slots:
                filho1.encontros[slot] = {}
                filho2.encontros[slot] = {}
                for turma in t1:
                    filho1.encontros[slot][turma] = pai1.encontros[slot][turma]
                    filho2.encontros[slot][turma] = pai2.encontros[slot][turma]
                for turma in t2:
                    filho1.encontros[slot][turma] = pai2.encontros[slot][turma]
                    filho2.encontros[slot][turma] = pai1.encontros[slot][turma]
            """
                    
            
            
            """
            showEncontros(filho1.encontros)
            showEncontros(filho2.encontros)
            """
            
            
            filhos.append(filho1)
            filhos.append(filho2)
    elif  opcoes['metodoCrossover'] == '2px':
        while pais != []:
            #escolhe ponto de cruzamento
            pontoCruzamento1 = randint(0,quantidadeTurmas-1)
            pontoCruzamento2 = randint(0,quantidadeTurmas-1)
            
            if pontoCruzamento2 > pontoCruzamento1:
                pontoCruzamento1, pontoCruzamento2 = pontoCruzamento2, pontoCruzamento1
            pai1 = choice(pais)
            pais.remove(pai1)
            pai2 = choice(pais)
            pais.remove(pai2)
            
            filho1 = CelulaAlg(grade)
            filho2 = CelulaAlg(grade)
            slots = pai1.encontros.keys()
            
            
            for slot in slots:
                encontrosPai1 = pai1.encontros[slot].items()
                encontrosPai2 = pai2.encontros[slot].items()
                filho1.encontros[slot] = dict(encontrosPai1[0:pontoCruzamento1] + encontrosPai2[pontoCruzamento1:pontoCruzamento2]+ encontrosPai1[pontoCruzamento2:]) 
                filho2.encontros[slot] = dict(encontrosPai2[0:pontoCruzamento1] + encontrosPai1[pontoCruzamento1:pontoCruzamento2]+ encontrosPai2[pontoCruzamento2:]) 
            
            
            
            filhos.append(filho1)
            filhos.append(filho2)
    elif  opcoes['metodoCrossover'] == 'sx':
        while pais != []:
            pai1 = choice(pais)
            pais.remove(pai1)
            pai2 = choice(pais)
            pais.remove(pai2)
            
            #showEncontros(pai1.encontros,'saida')
            #showEncontros(pai2.encontros,'saida')
            
            
            mascara = {}
            for turma in turmas:
                mascara[turma] = choice([0,1])
            print mascara
            
            
            filho1 = CelulaAlg(grade)
            filho2 = CelulaAlg(grade)
            slots = pai1.encontros.keys()
            
            
            for slot in slots:
                filho1.encontros[slot] = {}
                filho2.encontros[slot] = {}
                encontrosPai1 = pai1.encontros[slot].items()
                encontrosPai2 = pai2.encontros[slot].items()
                for turma in turmas:
                    if mascara[turma]:
                        filho1.encontros[slot][turma] = pai1.encontros[slot][turma]
                        filho2.encontros[slot][turma] = pai2.encontros[slot][turma]
                    else:
                        filho1.encontros[slot][turma] = pai2.encontros[slot][turma]
                        filho2.encontros[slot][turma] = pai1.encontros[slot][turma]
                        
                    
                    
                #filho1.encontros[slot] = dict(encontrosPai1[0:pontoCruzamento1] + encontrosPai2[pontoCruzamento1:pontoCruzamento2]+ encontrosPai1[pontoCruzamento2:]) 
                #filho2.encontros[slot] = dict(encontrosPai2[0:pontoCruzamento1] + encontrosPai1[pontoCruzamento1:pontoCruzamento2]+ encontrosPai2[pontoCruzamento2:]) 
            
            
            #showEncontros(filho1.encontros,'saida')
            #showEncontros(filho2.encontros,'saida')
            
            filhos.append(filho1)
            filhos.append(filho2)
    else:
        print 'Método de cruzamento inválido'
                    
    return filhos
    




def mutacao(individuos,opcoes):
    probabilidadeMutacao = float(opcoes['probabilidadeMutacao'])/1000
    #opcoes['metodoMutacao'] = 'trocarEncontro'
    #opcoes['metodoMutacao'] = 'trocarSlots'
    
    for celula in individuos:
        if  random() < probabilidadeMutacao:
            """
            Sorteia 2 slots 
            sorteia um encontro do primeiro slot
            a seguir seleciona o encontro do segundo slot cuja aula é compatível com a turma do encontro selecionado
            
            """
            
            #showEncontros(celula.encontros)
            if opcoes['metodoMutacao'] == 'trocarEncontro':
                slot1,slot2 = sample(celula.encontros.values(),2)
                encontroA = choice(slot1.values())
                encontroB = slot2[encontroA.aula.turma]
                        
                #troca as aulas dos encontros selecionados
                aulaAux = encontroA.aula
                encontroA.aula = encontroB.aula
                encontroB.aula = aulaAux
            if opcoes['metodoMutacao'] == 'trocarEncontroHeuristico':
                
                ##
                ##  Troca aulas com slot vizinho
                ##
                conj_slots = celula.encontros.values()
                tam = len(conj_slots)
                indice = choice(range(tam))
                slot1 = conj_slots[indice]
                slot2 = conj_slots[(indice+1)%tam]
                encontroA = choice(slot1.values())
                encontroB = slot2[encontroA.aula.turma]
                        
                #troca as aulas dos encontros selecionados
                aulaAux = encontroA.aula
                encontroA.aula = encontroB.aula
                encontroB.aula = aulaAux
            elif opcoes['metodoMutacao'] == 'trocarSlots':
            
                slot1,slot2 = sample(celula.encontros.keys(),2)
                aux = celula.encontros[slot1]
                celula.encontros[slot1] = celula.encontros[slot2]
                celula.encontros[slot2] = aux
            #showEncontros(celula.encontros)





def salvarProgresso(populacao,diretorioSaida,opcoes):
    print 'geracao: ',populacao['geracao'],'\tmelhor:',populacao['melhorFitness'],'\tmedia:',populacao['fitnessMedio'],'\desvio_padrao:',populacao['desvio_padrao']
    """
    for (key,value) in status.items():
        print key,':',value, '\t|',
    print ''
    
    """
    #f = open(str(grade)+str(grade.id)+'.csv','a')
    
    if not os.path.exists(diretorioSaida):
        os.makedirs(diretorioSaida)
    f = open(os.path.join(diretorioSaida, 'data.csv'),'a')
    
    writer = DictWriter(f,['geracao','qtd_individuos','melhorFitness','fitnessMedio','desvio_padrao'],extrasaction='ignore')
    writer.writerow(populacao)
    f.close()

    
    
    
def iniciarControladorProgresso(diretorioSaida):
    #f = open(str(grade)+str(grade.id)+'.csv','w')
    
    if not os.path.exists(diretorioSaida):
        os.makedirs(diretorioSaida)
    f = open(os.path.join(diretorioSaida, 'data.csv'),'w')
    #writer = DictWriter(f,['geracao','qtd_individuos','melhorFitness','fitnessMedio','desvio_padrao'])
    f.close()
    
    
    
def encerrarControladorProgresso(diretorioSaida,opcoes,celulaId,melhorIndividuo):



    # This is a demo of creating a pdf file with several pages.
    try:
        import datetime
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib
        from matplotlib.backends.backend_pdf import PdfPages
        import pylab
    except:
        print "ERRO, problema ao importar um dos pacotes:\n datetime, numpy, matplotlib, pylab"
        return
    
    cores = ['b-o','g--','r-s','c-^','m-D','y-x','k-*']
    
    # Create the PdfPages object to which we will save the pages:
    f = open(os.path.join(diretorioSaida, 'data.csv'),'r')
    #writer = DictWriter(f,status.keys())
    
    
    reader = DictReader(f,['geracao','qtd_individuos','melhorFitness','fitnessMedio','desvio_padrao'])
    
    dados = {}
    
    for key in reader.fieldnames:
        dados[key] = []
    for row in reader:
        for key in reader.fieldnames:
            dados[key].append(row[key])
    
    pdf = PdfPages(os.path.join(diretorioSaida,'grafico.pdf'))

    figure = pylab.figure(figsize=(20,20))
    
    
    pylab.plot()
    pylab.plot(dados['geracao'], dados['fitnessMedio'],  cores.pop(),label ='Fitness Medio')
    pylab.plot(dados['geracao'], dados['melhorFitness'],  cores.pop(),label ='Melhor Fitness')
    pylab.plot(dados['geracao'], dados['desvio_padrao'],  cores.pop(),label ='Desvio Padrao')
    pylab.plot(melhorIndividuo['geracao'], melhorIndividuo['individuo'].fitness,  cores.pop(),label ='Desvio Padrao')
    #pylab.plot(dados['geracao'], dados['tamanhoPopulacao'],  'b-o',label ='Tamanho Populacao')
    pylab.title('Celula '+str(celulaId))
    pylab.legend(loc=4) #posiciona a legendaem baixoa direita
    
    
    
    txt = ''
    for key,value in opcoes.iteritems():
        txt+=key+' '+str(value)+'\n'
    figure.text(.15,.8,txt)
    #pylab.set_xlabel('Geracao')
    #pylab.set_xlabel('Fitness')
    pylab.savefig(pdf, format='pdf') # note the format='pdf' argument!
    
    
    pylab.close()

    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Multipage PDF Example'
    d['Author'] = u'Jouni K. Sepp\xe4nen'
    d['Subject'] = 'How to create a multipage pdf file and set its metadata'
    d['Keywords'] = 'PdfPages multipage keywords author title subject'
    d['CreationDate'] = datetime.datetime(2009,11,13)
    d['ModDate'] = datetime.datetime.today()

    # Remember to close the object - otherwise the file will not be usable
    pdf.close()

    
def salvarTempos(diretorioSaida,tempos):

    # This is a demo of creating a pdf file with several pages.

    # This is a demo of creating a pdf file with several pages.
    try:
        import datetime
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib
        from matplotlib.backends.backend_pdf import PdfPages
        import pylab
    except:
        print "ERRO, problema ao importar um dos pacotes:\n datetime, numpy, matplotlib, pylab"
        return
        
    cores = ['b-o','g--','r-s','c-^','m-D','y-x','k-*']
    
    geracoes = range(len(tempos['avaliacao']))
    
    pdf = PdfPages(os.path.join(diretorioSaida,'tempo.pdf'))

    pylab.figure(figsize=(20,20))
    
    
    pylab.plot()
    for key,dados in tempos.iteritems():
        #pylab.plot(geracoes, dados,'r-o',label =key)
        pylab.plot(geracoes, dados,cores.pop(),label =key)
        
        
    #pylab.plot(dados['geracao'], dados['tamanhoPopulacao'],  'b-o',label ='Tamanho Populacao')
    pylab.title('Page One')
    pylab.legend()
    #pylab.set_xlabel('Geracao')
    #pylab.set_xlabel('Fitness')
    pylab.savefig(pdf, format='pdf') # note the format='pdf' argument!
    pylab.close()

    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Multipage PDF Example'
    d['Author'] = u'Jouni K. Sepp\xe4nen'
    d['Subject'] = 'How to create a multipage pdf file and set its metadata'
    d['Keywords'] = 'PdfPages multipage keywords author title subject'
    d['CreationDate'] = datetime.datetime(2009,11,13)
    d['ModDate'] = datetime.datetime.today()

    # Remember to close the object - otherwise the file will not be usable
    pdf.close()

    
    
    

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
            
    
    
    aulasProfessorTurma = {}
    for professor in totalAulasProfessor.keys():
        aulasProfessorTurma[professor] = {}
        for turma in turmas:
            aulasProfessorTurma[professor][turma] =  0
    
    for turma,aulasTurma in aulas.iteritems():
        for aula in aulasTurma:
            aulasProfessorTurma[aula.professor][turma] += aula.quantidade
    
    
    minimoDiasProfessor = {}
    for professor in totalAulasProfessor.keys():
        minimoDiasProfessor[professor] = 0
        
    for professor,turmas in aulasProfessorTurma.iteritems():
        
        for turma, quantidade in turmas.iteritems():
            if math.ceil(float(quantidade)/maxAulasPorDia) > minimoDiasProfessor[professor]:
                minimoDiasProfessor[professor] = math.ceil(float(quantidade)/maxAulasPorDia)
        if math.ceil(float(totalAulasProfessor[professor])/grade.auladia) > minimoDiasProfessor[professor]:
            minimoDiasProfessor[professor] = math.ceil(float(totalAulasProfessor[professor])/grade.auladia)
        
    import pprint
    pprint.pprint(minimoDiasProfessor)
    
    
    #print tipoRestricaoProfessorNoSlot
    return turmas,quantidadeTurmas,aulas,slots,tipoRestricaoProfessorNoSlot,minimoDiasProfessor
    


def populacaoInicial(grade,turmas,aulas,slots,tipoRestricaoProfessorNoSlot,opcoes):
    #POPULACAO INICIAL
    populacao = {}
    populacao['individuos'] = []
    for i in range(opcoes['populacao']):
        celula = criarCelula(grade,turmas,aulas,slots,tipoRestricaoProfessorNoSlot,opcoes)
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
    
    turmas,quantidadeTurmas,aulas,slots,tipoRestricaoProfessorNoSlot,minimoDiasProfessor = carregarDados(grade)
    
    #POPULACAO INICIAL
    populacao = populacaoInicial(grade,turmas,aulas,slots,tipoRestricaoProfessorNoSlot,opcoes)
        
    for celula in populacao['individuos']:
        avaliacao(celula,grade,turmas,aulas,slots,tipoRestricaoProfessorNoSlot,minimoDiasProfessor)
    
    
    melhorIndividuo = {}
    melhorIndividuo['individuo'] = populacao['individuos'][0]
    melhorIndividuo['geracao'] = 0
    
    populacao['melhorIndividuo'] = populacao['individuos'][0]
    populacao['melhorFitness'] = populacao['melhorIndividuo'].fitness
    populacao['fitnessTotal'] = 0
    populacao['tempoInicial'] = time()
    
    
    #localTime = localTime()
    data = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    print data
    
    diretorioSaida = 'saida/grade-'+str(grade.id)+'/tmp'
    
    iniciarControladorProgresso(diretorioSaida)
    #ENQUANTO  CRITERIOS DE PARADA NÃO FOREM SATISFEITOS REPETE-SE AS AÇÕES
    
    tempos = {}
    tiposTempo = ['selecao','crossover','mutacao','avaliacao','sobrevivencia']
    for tipo in tiposTempo:
        tempos[tipo] = []
        
    while not(fimDoAlgoritmo(populacao,opcoes)):
        
        tempoInicial = time()
        
        
        
        populacao['fitnessTotal'] = 0
        populacao['melhorIndividuo'] = populacao['individuos'][0]
        for celula in populacao['individuos']:
            populacao['fitnessTotal'] += celula.fitness
            if celula.fitness > populacao['melhorIndividuo'].fitness:
                populacao['melhorIndividuo'] = celula
                populacao['melhorFitness'] = populacao['melhorIndividuo'].fitness
                
        # se o melhor individuo da populacao for melhor que o melhor individuo ja encontrado
        # substitui o melhor individuo ja encontrado
        if populacao['melhorIndividuo'].fitness > melhorIndividuo['individuo'].fitness:
            melhorIndividuo['individuo'] = populacao['melhorIndividuo']
            melhorIndividuo['geracao'] = populacao['geracao']
            showEncontros(melhorIndividuo['individuo'].encontros,diretorioSaida)            
            
        populacao['qtd_individuos'] = len(populacao['individuos'])
        populacao['fitnessMedio'] = populacao['fitnessTotal'] / float(populacao['qtd_individuos'])
        aux = 0
        populacao['variancia'] = 0

        for celula in populacao['individuos']:
            aux += math.pow( (celula.fitness - populacao['fitnessMedio']), 2)
        
        populacao['variancia'] = aux / float(populacao['qtd_individuos'])
        
        populacao['desvio_padrao'] = math.sqrt(populacao['variancia'])

        
        salvarProgresso(populacao,diretorioSaida,opcoes)
        
        
        
        tempoInicial = time()
        
        #seleciona pais para cruzamento removendo-os do conjunto de individuos
        pais = selecao(populacao, opcoes)
        
        tempos['selecao'].append(time()-tempoInicial)
        tempoInicial = time()
        
        filhos = crossover(deepcopy(pais), opcoes, quantidadeTurmas,grade,turmas,diretorioSaida)
        
        
        tempos['crossover'].append(time()-tempoInicial)
        tempoInicial = time()
        
        mutacao(filhos, opcoes)
        
        tempos['mutacao'].append(time()-tempoInicial)
        tempoInicial = time()
        
        #avalia filhos gerados
        for celula in filhos:
            avaliacao(celula,grade,turmas,aulas,slots,tipoRestricaoProfessorNoSlot,minimoDiasProfessor)
            
        
        tempos['avaliacao'].append(time()-tempoInicial)
        tempoInicial = time()
        
        
        #
        # ATUALIZA CONJUNTO DE INDIVÍDUOS DA POPULAÇÃO
        
            
        """
        s = random()
        #print s * 100
        if s*100 < opcoes['chanceSobrevivencia']: 
            #SIMPLESMENTE SUBSTITUI OS PAIS PELOS FILHOS
            populacao['individuos'] += filhos
            populacao['individuos'] = sorted(populacao['individuos'], key=lambda c: c.fitness)[::-1]
        else:
            #SELECIONA OS MELHORES ENTRE PAIS E FILHOS
            candidatos = pais + filhos
            candidatos = sorted(candidatos, key=lambda c: c.fitness)[::-1]
            populacao['individuos'] += candidatos[0:len(pais)]
        """
        
        #escolhe os melhores entre pais e filhos
        
        #print s * 100
        if opcoes['metodoSobrevivencia'] == 'somenteFilhos': 
            #SIMPLESMENTE SUBSTITUI OS PAIS PELOS FILHOS
            populacao['individuos'] += filhos
            populacao['individuos'] = sorted(populacao['individuos'], key=lambda c: c.fitness)[::-1]
        elif opcoes['metodoSobrevivencia'] == 'somenteMelhores':
            #SELECIONA OS MELHORES ENTRE PAIS E FILHOS
            candidatos = pais + filhos
            candidatos = sorted(candidatos, key=lambda c: c.fitness)[::-1]
            populacao['individuos'] += candidatos[0:len(pais)]
        elif opcoes['metodoSobrevivencia'] == 'elitismo':
            tamanhoElite  = opcoes['tamanhoElite']
            candidatos = pais + filhos
            candidatos = sorted(candidatos, key=lambda c: c.fitness)[::-1]
            filhos = sorted(filhos, key=lambda c: c.fitness)[::-1]
            elite = candidatos[0:tamanhoElite]
            #uni elite e filhos a elite, descartando os piores filhos
            populacao['individuos'] += elite + filhos[0:-tamanhoElite]
        
        
            
            
            
            
        tempos['sobrevivencia'].append(time()-tempoInicial)
        tempoInicial = time()
        
        
        populacao['geracao'] += 1
        
    
    salvarTempos(diretorioSaida,tempos)
    print 'tempo final: ', time() - populacao['tempoInicial']
    #print 'Tempo para avaliar populacao de tamanho',opcoes['populacao'],': ',time()-inicio
    #inicio = time()
    
    newCel = melhorIndividuo['individuo'].save()
    arquivoSaida = open(os.path.join(diretorioSaida, 'config.txt'),'w')
    arquivoSaida.write(str(opcoes))
    arquivoSaida.close()
    encerrarControladorProgresso(diretorioSaida,opcoes,newCel.id,melhorIndividuo)

    os.rename(diretorioSaida,'saida/grade-'+str(grade.id)+'/'+str(newCel.id))
