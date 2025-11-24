from django.contrib import admin
from .models import Videojuego,Categoria

# Register your models here.
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ['nombre','mostrar_categorias']
    filter_horizontal = ['categorias']
    
    def mostrar_categorias(self,obj):
        return ", ".join([categoria.nombre for categoria in obj.categorias.all()])
    mostrar_categorias.short_description = 'Categorias'

admin.site.register(Videojuego,VideojuegoAdmin)
admin.site.register(Categoria)
