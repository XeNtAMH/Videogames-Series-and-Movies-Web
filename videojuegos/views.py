from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render,redirect,get_object_or_404
from .models import Videojuego
from calificacion.models import Calificacion 
from calificacion.forms import CalificacionForm

# Create your views here.

def home(request):
    return render(request,"home.html")

def videojuegos(request):
    videojuegos=Videojuego.objects.all()
    return render(request,'videojuegos.html',{"videojuegos":videojuegos})

def signup(request):
    #register user
    if request.method=='GET':
        return render(request, "SignUp.html",{
        'form':UserCreationForm,
    })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user=User.objects.create_user(username=request.POST["username"],password=request.POST["password1"])
                user.save()
                login(request,user)
                return redirect("videojuegos")
            except IntegrityError:
                return render(request, "SignUp.html",{
                    'form':UserCreationForm,
                    'error':"Usuario ya existe",
                })
        return render(request, "SignUp.html",{
                    'form':UserCreationForm,
                    'error':"Contrasenas no coinciden",
                })

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method=="GET":
        return render(request,'signin.html',{
            'form':AuthenticationForm
        })
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        
        if user is None:
            return render(request,'signin.html',{
            'form':AuthenticationForm,
            'error':"Usuario o contrasenas incorrectos",
        })
        else:
            login(request,user)
            return redirect('videojuegos')

def videojuegosdetail(request,id):
    videogame=get_object_or_404(Videojuego.objects.prefetch_related('categorias'),pk=id)
    
    # --- Lógica para preparar la calificación (para el GET) ---
    calificacion_actual = 0
    if request.user.is_authenticated:
        try:
            # Obtener la calificación actual del usuario
            calif_obj = Calificacion.objects.get(usuario=request.user, videojuego=videogame)
            calificacion_actual = calif_obj.puntuacion
        except Calificacion.DoesNotExist:
            pass
            
    # Crear el formulario, pre-llenando los campos ocultos
    rating_form = CalificacionForm(initial={
        'contenido_id': videogame.id,
        'tipo_contenido': 'videojuego' # Identificador clave para calificacion/views.py
    })

    context = {
        'videogame': videogame,
        'rating_form': rating_form,
        'calificacion_actual': calificacion_actual,
    }
    
    return render(request, "videojuegoDetail.html", context)
