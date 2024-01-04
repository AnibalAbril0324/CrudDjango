from django.shortcuts import render, redirect,get_object_or_404

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError #se importa para un control de error especifico
from .forms import TaskForm
from .models import Estudiante
from django.contrib.auth.decorators import login_required  # Este es un decorador muy útil en Django que asegura que una vista solo sea accesible para usuarios autenticados.

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
                    
@login_required
def tasks(request):
    estudiante=Estudiante.objects.filter(user=request.user)
    print(estudiante)
    # task es el areglo que envio a la tasks.html 
    return render(request, 'tasks.html',{'tasks':estudiante})

@login_required
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

@login_required        
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

@login_required
def crearpersona_detalle(request,task_id):
    if request.method == 'GET':
        task= get_object_or_404(Estudiante,pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        print(task_id)
        return render(request,'crear_personadetalles.html',{'task':task,'form'  :form})
    else:
        try:
            task= get_object_or_404(Estudiante,pk=task_id, user=request.user)
            form = TaskForm(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'crear_personadetalles.html',{'task':task,'form':form,
            'error':'Por favor ingrese datos validos'})  

@login_required
def delete_persona(request, task_id):
    task= get_object_or_404(Estudiante,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')