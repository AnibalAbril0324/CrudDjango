from django.forms import ModelForm
from .models import Estudiante


class TaskForm(ModelForm):
    class Meta:
        model = Estudiante 
        fields = ['cedula','nombre','apellido','direccion','telefono','user']      