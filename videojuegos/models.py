from django.db import models
from django.urls import reverse
from django.db.models import Avg

# Create your models here.
class Categoria(models.Model):
    nombre=models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Videojuego(models.Model):
    nombre=models.CharField(max_length=50)
    descripcion=models.TextField()
    categorias=models.ManyToManyField(Categoria)
    imagen=models.ImageField()
    precio=models.IntegerField()
    anio_lanzamiento = models.IntegerField(default=2000)
    
    def __str__(self):
        return self.nombre
    
    def tiene_categorias(self):
        return self.categorias.exists()
    
    def lista_categorias(self):
        return list(self.categorias.values_list('nombre'))
    
    def get_absolute_url(self):
        # Usa el nombre de la ruta definido en urls.py: name="videojuegosdetail"
        # Le pasamos el 'id' del objeto como argumento (kwargs={'id': self.id})
        return reverse('videojuegosdetail', kwargs={'id': self.id})

    @property
    def promedio_calificacion(self):
        # Accede al Calificacion_set (definido en calificacion/models.py)
        avg = self.calificacion_set.aggregate(Avg('puntuacion'))['puntuacion__avg']
        return round(avg, 1) if avg is not None else 0.0

    @property
    def porcentaje_estrellas(self):
        avg = self.promedio_calificacion
        # Devuelve el porcentaje para el CSS (promedio / 5 * 100)
        # Devolvemos un entero 0-100 para evitar problemas de localización
        return int(round((avg / 5) * 100)) if avg > 0 else 0