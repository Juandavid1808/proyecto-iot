from django.contrib import admin

from .models import (
    Usuario,
    Dispositivo,
    DatoSensor,
    Alerta
)

admin.site.register(Usuario)
admin.site.register(Dispositivo)
admin.site.register(DatoSensor)
admin.site.register(Alerta)