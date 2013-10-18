# -*- coding: utf-8 -*- 
"""
    Armazena conjunto de variaveis globais
    e confuguracoes do aplicativo
"""
dias_da_semana = ["SEG","TER","QUA","QUI","SEX","SAB","DOM"]
tipos = ["Indisponivel","Indesejavel","Disponivel"]
disciplinasPadrao = [   {'nome':'Artes'     , 'label':'ART'},
                        {'nome':'Biologia'  , 'label':'BIO'},
                        {'nome':'Ciências',   'label':'CIE'},
                        {'nome':'Educação Física', 'label':  'EFI'},
                        {'nome':'Ensino Religioso', 'label':  'ERE'},
                        #{'nome':'Espanhol'  , 'label':'ESP'},
                        {'nome':'Filosofia' , 'label':'FIL'},
                        {'nome':'Física'    , 'label':'FIS'},
                        {'nome':'Geografia' , 'label':'GEO'},
                        #{'nome':'Gramática' , 'label':'GRA'},
                        {'nome':'História'  , 'label':'HIS'},
                        {'nome':'Inglês'    , 'label':'ING'},
                        #{'nome':'Literatura', 'label':'LIT'},
                        {'nome':'Matemática', 'label':'MAT'},
                        {'nome':'Portugues' , 'label':'POR'},
                        {'nome':'Química'   , 'label':'QUI'},
                        #{'nome':'Redação'   , 'label':'RED'},
                        {'nome':'Sociologia', 'label':'SOC'}]
                        
                        
                        
pesos = {'professorInviavel'        :20,
        'choqueProfessores'       :15,
#        'professorIndesejavel'     :9,
        'excessoAulasNoMesmoDia'   :10,   
        'professoresComExcessoDias':8,
        'professorIndesejavel'     :5,
        'janelas'                  :1
        }
              
              
              
              
#penalidadesPonderadas 875.0 {'janelas': 14, 'excessoAulasNoMesmoDia': 11, 'choqueProfessores': 33, 'professorInviavel': 2, 'professorIndesejavel': 7, 'professoresComExcessoDias': 8.0}
#penalidadesPonderadas 882.0 {'janelas': 15, 'excessoAulasNoMesmoDia': 10, 'choqueProfessores': 32, 'professorInviavel': 2, 'professorIndesejavel': 8, 'professoresComExcessoDias': 9.0}

              
              
              
"""             
pesos = {'choqueProfessores'       :4,
        'professorInviavel'        :4,
        'professorIndesejavel'     :1,
        'janelas'                  :1,
        'professoresComExcessoDias':2,
        'excessoAulasNoMesmoDia': 3     
        }
        
        
pesos = {'choqueProfessores'       :10,
        'professorInviavel'        :10,
        'professorIndesejavel'     :4,
        'janelas'                  :1,
        'professoresComExcessoDias':8,
        'excessoAulasNoMesmoDia'   :8     
        }                
"""     

configuracaoPadrao = {'populacao'       :100,
                      'populacao_maior_tamanho' :  1000,
                      'populacao_menor_tamanho' :  10,
                      'limiteGeracoes'  :100000,
                      'limiteTempo'      :20,
                      'metodoSelecao'    :'torneio',
                      #'metodoSelecao'   :'aleatorio',
                      'metodoCrossover'  :'2px',
                      'metodoMutacao'    :'trocarEncontro',
                      'metodoSobrevivencia'    :'elitismo',
                      'tamanhoElite'     : 1,
                      'quantidadePais'   : 75,
                      'quantidadePais_maior_tamanho'   : 100,
                      'quantidadePais_menor_tamanho'   : 10,
                      'probabilidadeMutacao'   : 100,
                      'probabilidadeMutacao_maior_tamanho'   : 1000,
                      'probabilidadeMutacao_menor_tamanho'   : 1,
                      }
                      
maxAulasPorDia = 2
