# -*- coding: utf-8 -*-
from django.db import models
#from django.contrib.auth.models import User
from grades.models import Slot
from professores.models import Professor



# Create your models here.
class Restricao(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    tipo = models.IntegerField()
    professor = models.ForeignKey(Professor)
    slot = models.ForeignKey(Slot)
    def __unicode__(self):
        return "Professor: "+str(self.professor.id)+" Slot: "+str(self.slot)+" Tipo: "+str(self.tipo)

TIPO_RESTRICAO_PADRAO = 2

def addRestricoesPadrao(grade,professor):
    for slot in grade.slot_set.all():
        restricao = Restricao()
        restricao.slot = slot
        restricao.professor = professor
        restricao.tipo = TIPO_RESTRICAO_PADRAO
        restricao.save()
        

