from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Estudiante (models.Model):
    cedula =models.CharField(max_length=10)
    nombre =models.TextField(blank=True,max_length=50)
    apellido=models.TextField(blank=True,max_length=50)
    direccion=models.TextField(blank=True,max_length=100) 
    telefono=models.TextField(blank=True,max_length=10)
    user = models.ForeignKey(User,on_delete=models.CASCADE)     

    def __str__(self):
        return self.nombre+" "+self.apellido+"      by "+self.user.username