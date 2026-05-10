from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # Panel administrador Django
    path('admin/', admin.site.urls),

    # Rutas de AulaSmart
    path('api/', include('AulaSmart.urls')),

]