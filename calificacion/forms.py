# calificacion/forms.py

from django import forms

class CalificacionForm(forms.Form):
    # Puntuación: el valor de la estrella seleccionada (oculto, lo llena JS)
    puntuacion = forms.IntegerField(min_value=1, max_value=5, widget=forms.HiddenInput())
    # ID del elemento (videojuego, serie o peli)
    contenido_id = forms.IntegerField(widget=forms.HiddenInput())
    # Tipo de elemento ('videojuego', 'serie' o 'pelicula')
    tipo_contenido = forms.CharField(max_length=20, widget=forms.HiddenInput())