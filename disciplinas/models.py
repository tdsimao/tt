# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Disciplina(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    nome = models.CharField(max_length=45)
    label = models.CharField(max_length=45)
    user = models.ForeignKey(User)    
    def __unicode__(self):
        return self.label