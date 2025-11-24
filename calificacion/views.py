# calificacion/views.py

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Importar modelos de las otras apps
from videojuegos.models import Videojuego 
from series.models import Serie
from peliculas.models import Pelicula
from .models import Calificacion # Modelo de esta misma app
from .forms import CalificacionForm # Formulario de esta misma app

@login_required
def calificar_contenido(request):
    """
    Procesa el envío del formulario de calificación. 
    Esta vista maneja POST desde CUALQUIER página de detalle.
    """
    # Solo procesamos POST
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', '/'))

    form = CalificacionForm(request.POST)
    
    if form.is_valid():
        puntuacion = form.cleaned_data['puntuacion']
        contenido_id = form.cleaned_data['contenido_id']
        tipo_contenido = form.cleaned_data['tipo_contenido'] # 'videojuego', 'serie' o 'pelicula'
        usuario = request.user
        
        # 1. Determinar el Modelo y el campo FK a usar
        ModeloContenido = None
        campo_fk = None
        
        if tipo_contenido == 'videojuego':
            ModeloContenido = Videojuego
            campo_fk = 'videojuego'
        elif tipo_contenido == 'serie':
            ModeloContenido = Serie
            campo_fk = 'serie'
        elif tipo_contenido == 'pelicula':
            ModeloContenido = Pelicula
            campo_fk = 'pelicula'
        else:
            messages.error(request, "Tipo de contenido inválido para calificar.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # 2. Obtener el elemento de contenido
        try:
            contenido_objeto = get_object_or_404(ModeloContenido, pk=contenido_id)
        except Exception:
            messages.error(request, "El elemento a calificar no existe.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # 3. Crear o Actualizar la Calificación (update_or_create garantiza 1 voto)
        fk_data = {campo_fk: contenido_objeto} 
        
        Calificacion.objects.update_or_create(
            usuario=usuario,
            **fk_data, 
            defaults={'puntuacion': puntuacion}
        )
        
        messages.success(request, f"Tu calificación de {puntuacion} estrellas ha sido registrada o actualizada.")
        
        # 4. Redirigir al usuario de vuelta a la página de detalles
        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        messages.error(request, "Error en el envío de la calificación.")
        return redirect(request.META.get('HTTP_REFERER', '/'))