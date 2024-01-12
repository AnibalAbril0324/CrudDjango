from django import forms
from .models import Estudiante


class TaskForm(forms.ModelForm):
    class Meta:
        model = Estudiante 
        fields = ['cedula','nombre','apellido','direccion','telefono','user']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control' ,'placeholder':'Escribe tu cedula'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control' ,'placeholder':'Escribe tu nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control' ,'placeholder':'Escribe tu apellido'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control' ,'placeholder':'Escribe tu direccion'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control' ,'placeholder':'Escribe tu telefono'}),
        }       