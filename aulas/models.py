# -*- coding: utf-8 -*-
from django.db import models
from disciplinas.models import Disciplina
from professores.models import Professor
from turmas.models import Turma



# Create your models here.
class Aula(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    quantidade  = models.IntegerField()
    turma = models.ForeignKey(Turma)    
    disciplina = models.ForeignKey(Disciplina)  
    professor = models.ForeignKey(Professor)    
    def __unicode__(self):
        return str(self.id)