from django.shortcuts import render,redirect,get_object_or_404
from .models import Pelicula
from calificacion.models import Calificacion 
from calificacion.forms import CalificacionForm

# Create your views here.
def peliculas(request):
    peliculas=Pelicula.objects.all()
    return render(request,'peliculas.html',{"peliculas":peliculas})

def peliculasdetails(request,id):
    # La variable 'pelicula' será el objeto único.
    pelicula = get_object_or_404(Pelicula.objects.prefetch_related('categorias'),pk=id)
    
    # --- Lógica para preparar la calificación ---
    calificacion_actual = 0
    if request.user.is_authenticated:
        try:
            # Busca la calificación del usuario para esta película
            calif_obj = Calificacion.objects.get(usuario=request.user, pelicula=pelicula)
            calificacion_actual = calif_obj.puntuacion
        except Calificacion.DoesNotExist:
            pass
            
    # Crear el formulario, pre-llenando los campos ocultos
    rating_form = CalificacionForm(initial={
        'contenido_id': pelicula.id,
        'tipo_contenido': 'pelicula' # Identificador clave para calificacion/views.py
    })

    context = {
        'peliculas': pelicula, # Usamos 'peliculas' para mantener la consistencia con tu plantilla existente
        'rating_form': rating_form,
        'calificacion_actual': calificacion_actual,
    }

    return render(request, "peliculasdetails.html", context)