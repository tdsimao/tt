# -*- coding: utf-8 -*-
from django.db import models
#from django.contrib.auth.models import User
from grades.models import Grade



# Create your models here.
class Turma(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    nome = models.CharField(max_length=45)
    grade = models.ForeignKey(Grade)
    def __unicode__(self):
        return self.nome
    
    
    def totalAulas(self):
        totalAulas = 0
        for aula in self.aula_set.all():
            totalAulas = totalAulas + aula.quantidade
        return totalAulas
    
    def is_valid(self):
        """
            verifica se a turma cadastrada é valida
                    -número de aulas
        """
        if self.totalAulas() == self.grade.auladia * self.grade.dias:
            return True
        return False