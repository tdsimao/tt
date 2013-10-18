# -*- coding: utf-8 -*- 
from django import forms
from src.variaveisGlobais import configuracaoPadrao


class CreateCelulaForm(forms.Form):
    populacao = forms.IntegerField(initial = configuracaoPadrao['populacao'],
                                   label='Tamanho da população:',
                                   max_value=configuracaoPadrao['populacao_maior_tamanho'], 
                                   min_value=configuracaoPadrao['populacao_menor_tamanho']
                                    )
    limiteGeracoes = forms.IntegerField(initial = configuracaoPadrao['limiteGeracoes'],label='Critério  de parada - Limite de gerações:')
    limiteTempo = forms.FloatField(initial = configuracaoPadrao['limiteTempo'],
                                                label='Critério  de parada - Limite de tempo:',
                                                help_text='horas')
    metodoSelecao = forms.ChoiceField(initial = configuracaoPadrao['metodoSelecao'],label='Método de Seleção:',
                                    widget=forms.RadioSelect,
                                    choices=(
                                        ("torneio", "torneio"),
                                        ("roleta", "roleta"),
                                        ("aleatorio", "aleatorio"),
                                    ))
    quantidadePais = forms.IntegerField(initial = configuracaoPadrao['quantidadePais'],
                                        label='Quantidade de células selecionadas para crossover:',
                                        help_text='% da população',
                                        max_value=configuracaoPadrao['quantidadePais_maior_tamanho'], 
                                        min_value=configuracaoPadrao['quantidadePais_menor_tamanho'])
                                        
    metodoCrossover = forms.ChoiceField(initial = configuracaoPadrao['metodoCrossover'],label='Método de Crossover:',
                                    widget=forms.RadioSelect,
                                    choices=(
                                        ("1px", "1px"),
                                        ("2px", "2px"),
                                        ("sx", "sx"))
                                    )
    
    metodoMutacao = forms.ChoiceField(initial = configuracaoPadrao['metodoMutacao'],label='Método de Mutação:',
                                    widget=forms.RadioSelect,
                                    choices=(
                                        ("trocarEncontro", "trocarEncontro"),
                                        ("trocarSlots", "trocarSlots"),
                                        ("trocarEncontroHeuristico","trocarEncontroHeuristico"))
                                    )
    probabilidadeMutacao = forms.IntegerField(initial = configuracaoPadrao['probabilidadeMutacao'],
                                        label='Probabilidade de Mutacao em cada geração:',
                                        help_text='‰ de chance de ocorrer mutação',
                                        max_value=configuracaoPadrao['probabilidadeMutacao_maior_tamanho'], 
                                        min_value=configuracaoPadrao['probabilidadeMutacao_menor_tamanho'])
    metodoSobrevivencia = forms.ChoiceField(initial = configuracaoPadrao['metodoSobrevivencia'],label='Método de Sobrevivência:',
                                    widget=forms.RadioSelect,
                                    choices=(
                                        ("elitismo", "elitismo"),
                                        ("somenteFilhos", "somenteFilhos"),
                                        ("somenteMelhores", "somenteMelhores"))
                                    )
    tamanhoElite = forms.IntegerField(initial = configuracaoPadrao['tamanhoElite'],
                                    label='Tamanho da elite:',
                                    max_value=100, 
                                    min_value=0,
                                    help_text='0 sobrevivem uma amostra aleatoria, 100 apenas os melhores')
    repeticoes = forms.IntegerField(initial = 3,
                                        label='Quantidade de horarios a serem criados:',
                                        max_value=10, 
                                        min_value=0)