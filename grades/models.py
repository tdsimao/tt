# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Grade(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    escola = models.CharField(max_length=45)
    turno = models.CharField(max_length=45)
    dias = models.IntegerField()
    auladia = models.IntegerField()
    user = models.ForeignKey(User)
    ano = models.IntegerField(null = True)
    periodo = models.IntegerField(null = True)
    
    
    
    def __unicode__(self):
        return self.escola +' '+ self.turno
    
    def is_valid(self):
        """
            TODO:
                verificar se a grade cadastrada eh valida:
                    -numero de aulas por turma
                    -número de aulas por professor
        """
        if self.turma_set.all().count() == 0:
            return False
        for turma in self.turma_set.all():
            if not turma.is_valid():
                return False
        return True
        
    def setSlots(self):
        #==================================================
        #    Remove  slots cadastrados
        #    Cadastra novos slots
        #===================================================
        for slot in self.slot_set.all():
            slot.delete()
        for d in range(self.dias):
            for h in range(self.auladia):
                slot = Slot()
                slot.grade  = self
                slot.dia = d
                slot.horario = h
                slot.save()
                
    def getProfessores(self):
        """
            Retorna lista de professores que tem vinculo com a grade
            ou seja retorna professores que tem aula com as turmas da grade
        """
        professores = []
        for turma in self.turma_set.all():
            for aula in turma.aula_set.all():
                if aula.professor not in professores:
                    professores.append(aula.professor)
                
        return professores





class Slot(models.Model):
    __tablename__ = 'slot'
    
    id = models.AutoField(primary_key = True, unique = True)
    grade = models.ForeignKey(Grade)
    dia = models.IntegerField()
    horario = models.IntegerField()

    def __unicode__(self):
        return str(self.dia) +' '+ str(self.horario)
    
    
