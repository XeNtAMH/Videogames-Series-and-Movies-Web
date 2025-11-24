# calificacion/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator 

# Importamos los modelos de las otras aplicaciones para las relaciones
from videojuegos.models import Videojuego 
from series.models import Serie
from peliculas.models import Pelicula

class Calificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Relaciones para los tres tipos de contenido (solo una debe estar llena por objeto)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE, null=True, blank=True)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True, blank=True)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        # Esto asegura 1 voto por usuario para cada elemento, evitando duplicados
        unique_together = (
            ('usuario', 'videojuego'), 
            ('usuario', 'serie'), 
            ('usuario', 'pelicula')
        )
        
    def __str__(self):
        if self.videojuego:
            return f"{self.puntuacion} estrellas para {self.videojuego.nombre}"
        if self.serie:
            return f"{self.puntuacion} estrellas para {self.serie.nombre}"
        if self.pelicula:
            return f"{self.puntuacion} estrellas para {self.pelicula.nombre}"
        return f"Calificación de {self.puntuacion}"