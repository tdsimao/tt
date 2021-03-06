from django.db import models
from django.contrib.auth.models import User
from disciplinas.models import Disciplina    




# Create your models here.
class Professor(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    nome = models.CharField(max_length=45)
    label = models.CharField(max_length=45)
    user = models.ForeignKey(User)   
    disciplinas  = models.ManyToManyField(Disciplina)
    def __unicode__(self):
        return self.label

"""
    def getRestricoes(self,grade):
        restricoes = []
        for restricao in self.restricao_set.all():
            if restricao.slot in grade.slot_set.all():
                restricoes.append(restricao)
        return restricoes

"""