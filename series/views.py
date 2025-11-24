from django.shortcuts import render,redirect,get_object_or_404
from .models import Serie

# Create your views here.
def series(request):
    series=Serie.objects.all()
    return render(request,'series.html',{"series":series})

# series/views.py

from django.shortcuts import render,redirect,get_object_or_404
from .models import Serie
# NUEVO: Imports de la app calificacion
from calificacion.models import Calificacion 
from calificacion.forms import CalificacionForm 

# ... (otras vistas) ...

def seriesdetail(request,id):
    # Usamos 'serie' internamente, pero el contexto mantendrá 'series'
    serie = get_object_or_404(Serie.objects.prefetch_related('categorias'), pk=id)

    # --- Lógica para preparar la calificación ---
    calificacion_actual = 0
    if request.user.is_authenticated:
        try:
            # Busca la calificación del usuario para esta serie
            calif_obj = Calificacion.objects.get(usuario=request.user, serie=serie)
            calificacion_actual = calif_obj.puntuacion
        except Calificacion.DoesNotExist:
            pass
            
    # Crear el formulario, pre-llenando los campos ocultos
    rating_form = CalificacionForm(initial={
        'contenido_id': serie.id,
        'tipo_contenido': 'serie' # Identificador clave para calificacion/views.py
    })
    
    context = {
        'series': serie, # Mantenemos 'series' para no romper la plantilla existente
        'rating_form': rating_form,
        'calificacion_actual': calificacion_actual,
    }

    return render(request, "seriesDetail.html", context)