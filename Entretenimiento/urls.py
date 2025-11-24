"""
URL configuration for Entretenimiento project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from search.views import search,busqueda_dinamica
from videojuegos.views import videojuegos,home,signin,signup,signout,videojuegosdetail
from peliculas.views import peliculas,peliculasdetails
from series.views import series,seriesdetail
from calificacion.views import calificar_contenido
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name='home' ),
    path('admin/', admin.site.urls),
    path('search/',search, name='search'),
    path('busqueda-dinamica/',busqueda_dinamica, name='busqueda_dinamica'),
    path('videojuegos/',videojuegos,name='videojuegos'),
    path('videojuegos/<int:id>/',videojuegosdetail, name="videojuegosdetail"),
    path('peliculas/',peliculas,name='peliculas'),
    path('peliculas/<int:id>/',peliculasdetails, name="peliculasdetails"),
    path('series/',series,name='series'),
    path('series/<int:id>/',seriesdetail, name="seriesdetail"),
    path('calificar/',calificar_contenido, name='calificar_contenido'),
    path('signup/',signup, name="signup"),
    path('logout/',signout, name="logout"),
    path('signin/',signin, name="signin"),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)