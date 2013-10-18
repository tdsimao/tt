# -*- coding: utf-8 -*-
from django.db import models
#from django.contrib.auth.models import User
from grades.models import Grade,Slot
from aulas.models import Aula



class Celula(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    grade = models.ForeignKey(Grade)
    fitness  = models.FloatField(null = True)
    opcoes = models.TextField(null = True)
    encontros = {}
    """
    def __init__(self, *args, **kwargs):
        super(models.Model,self).__init__(*args, **kwargs)
        self.encontros = {}
    """
        
    def __unicode__(self):
        return str(self.fitness) 
    
    

    
    
class Encontro(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    celula = models.ForeignKey(Celula)
    slot = models.ForeignKey(Slot)
    aula = models.ForeignKey(Aula)
    def __unicode__(self):
        return str(self.aula.disciplina)+' / '+str(self.aula.professor.id)+' - dia'+str(self.slot.dia)
    
