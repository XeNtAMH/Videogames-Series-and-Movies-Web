from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from videojuegos.models import Videojuego
from series.models import Serie
from peliculas.models import Pelicula

# Vista principal para la plantilla de búsqueda
def search(request):
    return render(request, 'search.html')

# Vista que maneja la lógica de búsqueda dinámica (Fetch API)
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from videojuegos.models import Videojuego
from series.models import Serie
from peliculas.models import Pelicula

# Vista principal para la plantilla de búsqueda
def search(request):
    return render(request, 'search.html')

# Vista que maneja la lógica de búsqueda dinámica (Fetch API)
def busqueda_dinamica(request):
    query = request.GET.get('q', '').strip() 
    filtro = request.GET.get('filtro', 'todo') 
    resultados = []
    
    if query:
        # La Q-filter ahora se construye DENTRO de cada bloque para usar los campos correctos.
        
        # 1. Videojuegos
        if filtro in ['todo', 'videojuego']:
            try:
                # Consulta específica para Videojuego: busca en el campo 'nombre' O en las categorias
                juegos_q_filter = Q(nombre__icontains=query) | Q(categorias__nombre__icontains=query)
                juegos = Videojuego.objects.filter(juegos_q_filter).distinct()[:5]
                
                for item in juegos:
                    resultados.append({
                        'nombre': item.nombre,
                        'tipo': 'Videojuego',
                        'url': item.get_absolute_url() 
                    })
            except Exception as e:
                print(f"Error en Videojuegos: {e}")
                
        # 2. Series
        if filtro in ['todo', 'serie']:
            try:
                # Consulta para Series: ASUMIMOS que tiene campo 'nombre'.
                # SI tiene campo 'categorias', usa: Q(nombre__icontains=query) | Q(categorias__nombre__icontains=query)
                series_q_filter = Q(nombre__icontains=query)
                series = Serie.objects.filter(series_q_filter)[:5] 
                
                for item in series:
                    resultados.append({
                        'nombre': item.nombre,
                        'tipo': 'Serie',
                        'url': item.get_absolute_url() 
                    })
            except Exception as e:
                print(f"Error en Series: {e}")

        # 3. Películas
        if filtro in ['todo', 'pelicula']:
            try:
                # Consulta para Películas: ASUMIMOS que tiene campo 'nombre'.
                peliculas_q_filter = Q(nombre__icontains=query)
                peliculas = Pelicula.objects.filter(peliculas_q_filter)[:5]
                
                for item in peliculas:
                    resultados.append({
                        'nombre': item.nombre,
                        'tipo': 'Película',
                        'url': item.get_absolute_url() 
                    })
            except Exception as e:
                print(f"Error en Películas: {e}")

    # Devuelve los resultados en formato JSON
    return JsonResponse({'resultados': resultados})