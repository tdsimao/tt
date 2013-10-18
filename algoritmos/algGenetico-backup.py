# -*- coding: utf-8 -*- 
from celulas.models import Celula, Encontro
from random import choice, random, sample
from time import time
from src.variaveisGlobais import pesos


class CelulaAlg(Celula):
    """
        classe criada para acumular lista de encontros sem salva-los
        e editar o metodo save() permitindo salvar os encontros
    
    
    """
    encontros = {}
    
    def __init__(self, *args, **kwargs):
        super(Celula,self).__init__(*args, **kwargs)
        self.encontros = {}

    def save(self, *args, **kwargs):
        newCel = Celula()
        newCel.grade = self.grade
        newCel.fitness = self.fitness
        
        if getattr(self, 'commit', True):
            # Caso seja necessario salvar
            newCel.save()
            # salva tambem todos os encontros
            for slot in self.encontros.values():
                for encontro in slot:
                    encontro.celula = newCel
                    encontro.save()
        return newCel
    

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
    
    
    professores = totalAulasProfessor.keys()
    totalDiasProfessor = {}
    
    
    
    for dia in range(grade.dias):
        ultimaAula = {}
        professoresNoDia = []
        for horario in range(grade.auladia):
            slot = slots[dia*grade.dias+horario]
            professoresNoSlot = []
            
            for encontro in celula.encontros[slot]:
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
        professoresComExcessoDias = professoresComExcessoDias + (totalDiasProfessor[professor] - quantidadeAulas/grade.auladia)
    
    totalPenalidades = pesos['choqueProfessores'] * choqueProfessores + pesos['professorInviavel'] * professorInviavel + pesos['professorIndesejavel'] * professorIndesejavel + pesos['janelas'] * janelas + pesos['professoresComExcessoDias'] * professoresComExcessoDias
    
    
    celula.fitness = 1./(1.+totalPenalidades)


def criarCelula(grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot,opcoes):
    
    # cria uma celula que representa uma solucao para a grade
    # possui um conjunto de encontros
    # encontros sao definidos aleatoriamente
    celula = CelulaAlg(grade)
    
    celula.grade = grade
    
    for slot in slots:
        celula.encontros[slot] = []
    
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
            celula.encontros[slot].append(encontro)
        
    return celula
    
    
    
    
def fimDoAlgoritmo(populacao,opcoes):
    if populacao['geracao'] == opcoes['limiteGeracoes']:
        print 'Limite de Gerações Atingido'
        return True
    return False







def  selecao(populacao,opcoes):
    pais = []
    quantidadePais = (opcoes['populacao'] / 100) * opcoes['quantidadePais']
    print '-=-=-=-=-=-=-   ',quantidadePais
    if  opcoes['metodoSelecao'] == 'roleta':
        fitnessTotal  = 0
        for celula in populacao['individuos']:
            fitnessTotal = fitnessTotal + celula.fitness
        for i  in range():
            somaFitness = 0
            t = random() * fitnessTotal
            for celula in populacao['individuos']:
                if somaFitness > t and celula not in pais:
                    pais.append(celula)
                    break
                somaFitness = somaFitness + celula.fitness
    elif  opcoes['metodoSelecao'] == 'torneio':
        
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
            
    elif  opcoes['metodoSelecao'] == 'aleatorio':
        pais = sample(populacao['individuos'],opcoes['quantidadePais'])
            
    return pais



def crossover(pais,opcoes):
    filhos = []
    return filhos




def mutacao(populacao,opcoes):
    probabilidadeMutacao = float(opcoes['probabilidadeMutacao'])/100
    for celula in populacao['individuos']:
        if  random() < probabilidadeMutacao:
            """
            Sorteia 2 slots 
            sorteia um encontro do primeiro slot
            a seguir seleciona o encontro do segundo slot cuja aula é compatível com a turma do encontro selecionado
            
            """
            
            slot1,slot2 = sample(celula.encontros.values(),2)
            encontroA = choice(slot1)
            
            
            for encontro in slot2:
                if encontro.aula.turma == encontroA.aula.turma:
                    encontroB = encontro
                    
            #troca as aulas dos encontros selecionados
            aulaAux = encontroA.aula
            encontroA.aula = encontroB.aula
            encontroB.aula = aulaAux
            




def exportarEstadoAlgoritmo(statusList,grade):
    
    from csv import DictWriter as csvDictWriter
    f = open(str(grade)+str(grade.id)+'.csv','wb')
    writer = csvDictWriter(f,statusList[0].keys())
    writer.writeheader()
    writer.writerows(statusList)
    f.close()
    
def getStatus(populacao,opcoes):
    
    status = {}
    status['geracao'] = populacao['geracao'] 
    status['melhorFitness'] = populacao['melhorFitness'] 
    status['fitnessMedio'] = populacao['fitnessTotal']/opcoes['populacao']
    
    return(status)
    
    


def criarHorario(grade, opcoes):
    
    inicio = time()
    # TRAZ INFORMACOES DO BANCO DE DADOS PARA MEMORIA
    
    
    turmas = grade.turma_set.all()
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
    
    #TODO
    #  CHECAR SE A GRADE E VALIDA
    if not(grade.is_valid()):
        print 'Grade Invalida'
        return

    print 'Tempo para carregar dados ',time()-inicio
    inicio = time()
    
    
    
    #POPULACAO INICIAL
    populacao = {}
    populacao['individuos'] = []
    populacao['fitnessTotal'] = 0
    populacao['melhorFitness'] = 0
    for i in range(opcoes['populacao']):
        
        celula = criarCelula(grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot,opcoes)
        populacao['individuos'].append(celula)
        
    populacao['geracao'] = 0
    print 'Tempo de criacao da populacao inicial de tamanho ',opcoes['populacao'],': ',time()-inicio
    
    statusList = []
    
    #ENQUANTO  CRITERIOS DE PARADA NÃO FOREM SATISFEITOS REPETE-SE AS AÇÕES
    while not(fimDoAlgoritmo(populacao,opcoes)):
        print 'Geração ', populacao['geracao'],
        for celula in populacao['individuos']:
            avaliacao(celula,grade,turmas,aulas,totalAulasProfessor,slots,tipoRestricaoProfessorNoSlot)
            populacao['fitnessTotal'] += celula.fitness
            if celula.fitness > populacao['melhorFitness']:
                populacao['melhorFitness'] = celula.fitness
                populacao['melhorIndividuo'] = celula
        pais = selecao(populacao, opcoes)
        mutacao(populacao, opcoes)
        
        filhos = crossover(pais, opcoes)
        
        
        
        statusList.append(getStatus(populacao,opcoes))
        
        populacao['geracao'] += 1
    exportarEstadoAlgoritmo(statusList,grade)
    print 'Tempo para avaliar populacao de tamanho',opcoes['populacao'],': ',time()-inicio
    inicio = time()
    
    
    
    
    #BUSCA MELHOR CELULA
    melhorCelula = populacao['individuos'][0]
    
    melhoresCelulas = []
    melhoresCelulas.append(populacao['individuos'][0])
    for celula in populacao['individuos']:
        if celula.fitness > melhoresCelulas[0].fitness:
            melhoresCelulas = []
            melhoresCelulas.append(celula)
        elif celula.fitness == melhoresCelulas[0].fitness:
            melhoresCelulas.append(celula)
        if celula.fitness > melhorCelula.fitness:
            melhorCelula = celula
    print 'Tempo de selecao da melhor celula em uma populacao de tamanho ',opcoes['populacao'],': ',time()-inicio
    print 'melhores celulas: ',melhoresCelulas
    #SALVA APENAS MELHOR CELULA
    
    
    import pprint
    aux = str(pprint.pprint(opcoes))
    print aux
    aux = str(opcoes)
    print aux
    melhorCelula.save()
    
    
    
    