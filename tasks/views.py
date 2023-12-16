from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError #se importa para un control de error especifico
from .forms import TaskForm
from .models import Estudiante

def home(request):
    return render(request,'home.html')     

def singup(request):
    
    if request.method == 'GET':
        return render(request,'singup.html',{
        'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registro usuario
            try:
                user=User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save();
                # se coloca el mismo nombre que se le asigna en el path que esta
                # en el archivo urls.pv
                login(request,user)
                return redirect('tasks')

            except IntegrityError:
                 return render(request,'singup.html',{
                    'form' : UserCreationForm,
                    "error": 'User name already exists'
                 })
        return render(request,'singup.html',{
                    'form' : UserCreationForm,
                    "error": 'Password do not match'
                 })
      
def tasks(request):
    estudiante=Estudiante.objects.filter(user=request.user)
    print(estudiante)
    # task es el areglo que envio a la tasks.html 
    return render(request, 'tasks.html',{'tasks':estudiante})

def signout(request):
    logout(request)
    return redirect('home')

#le enviamos un diccionario para la autenticacion 
def singin(request):
    if request.method == 'GET':
        return  render (request,'singin.html',{
            'form': AuthenticationForm
        })
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])

        if user is None:
            return render(request,'singin.html',{
                'form': AuthenticationForm,
                'error':'Username or Password is incorrect'
            })
        else:
            login(request,user)
            return redirect('tasks')
        
def crear_persona (request):

    if request.method == 'GET':
        return render(request,'crear_persona.html',{
            'form':  TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user= request.user
            print(new_task)
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'crear_persona.html',{
                'form':TaskForm,
                'error':'Por favor ingrese datos validos'
            })