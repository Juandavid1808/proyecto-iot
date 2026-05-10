from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
        ('visor', 'Visor'),
    ]
    telefono = models.CharField(max_length=20, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='visor')

    groups = models.ManyToManyField(
        'auth.Group', related_name='usuario_set', blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='usuario_set', blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.rol})"


class Dispositivo(models.Model):
    nombre     = models.CharField(max_length=100)
    ubicacion  = models.CharField(max_length=200, blank=True, null=True)
    activo     = models.BooleanField(default=True)

    # Sensores físicos reales del prototipo
    sensor_temperatura_humedad = models.BooleanField(default=False, verbose_name='DHT22 - Temperatura/Humedad')
    sensor_sonido              = models.BooleanField(default=False, verbose_name='KY-038 - Sonido')
    sensor_luz                 = models.BooleanField(default=False, verbose_name='LDR - Luz')
    sensor_movimiento          = models.BooleanField(default=False, verbose_name='PIR HC-SR501 - Movimiento')

    propietario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name='dispositivos'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    # ─────────────────────────────────────────────
    # GET /api/dashboard/
    # ─────────────────────────────────────────────
    @method_decorator(csrf_exempt, name='dispatch')
    class DashboardView(View):

        def get(self, request):
            dispositivos = (
                Dispositivo.objects
                .filter(activo=True)
                .select_related('propietario')
                .prefetch_related(
                    'datos',
                    'alertas'
                )
            )

            resultado = []

            for dispositivo in dispositivos:
                datos = [
                    {
                        "id": dato.id,
                        "tipo_sensor": dato.tipo_sensor,
                        "valor": dato.valor,
                        "unidad": dato.unidad,
                        "timestamp": dato.timestamp.isoformat(),
                        "metadata": dato.metadata,
                    }
                    for dato in dispositivo.datos.all()[:10]
                ]

                alertas = [
                    {
                        "id": alerta.id,
                        "mensaje": alerta.mensaje,
                        "nivel": alerta.nivel,
                        "estado": alerta.estado,
                        "creada_en": alerta.creada_en.isoformat(),
                        "resuelta_en": alerta.resuelta_en.isoformat() if alerta.resuelta_en else None,
                    }
                    for alerta in dispositivo.alertas.all()[:10]
                ]

                resultado.append({
                    "id": dispositivo.id,
                    "nombre": dispositivo.nombre,
                    "ubicacion": dispositivo.ubicacion,
                    "activo": dispositivo.activo,

                    "propietario": {
                        "id": dispositivo.propietario.id if dispositivo.propietario else None,
                        "username": dispositivo.propietario.username if dispositivo.propietario else None,
                        "rol": dispositivo.propietario.rol if dispositivo.propietario else None,
                    },

                    "sensores": dispositivo.sensores_activos(),

                    "datos": datos,

                    "alertas": alertas,
                })

            return JsonResponse({
                "ok": True,
                "total": len(resultado),
                "dispositivos": resultado,
            })

    def sensores_activos(self):
        sensores = []
        if self.sensor_temperatura_humedad: sensores.append('temperatura')
        if self.sensor_temperatura_humedad: sensores.append('humedad')
        if self.sensor_sonido:              sensores.append('sonido')
        if self.sensor_luz:                 sensores.append('luz')
        if self.sensor_movimiento:          sensores.append('movimiento')
        return sensores

    def __str__(self):
        return f"{self.nombre} ({', '.join(self.sensores_activos()) or 'sin sensores'})"


class DatoSensor(models.Model):
    TIPO_SENSOR_CHOICES = [
        ('temperatura', 'Temperatura (DHT11)'),
        ('humedad',     'Humedad (DHT11)'),
        ('sonido',      'Sonido (KY-037)'),
        ('luz',         'Luz (LDR)'),
    ]
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='datos')
    tipo_sensor = models.CharField(max_length=20, choices=TIPO_SENSOR_CHOICES)
    valor       = models.FloatField()
    unidad      = models.CharField(max_length=20, default='')
    timestamp   = models.DateTimeField(auto_now_add=True)
    metadata    = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.dispositivo.nombre} [{self.tipo_sensor}]: {self.valor} {self.unidad}"


class Alerta(models.Model):
    NIVEL_CHOICES = [
        ('info',        'Informativo'),
        ('advertencia', 'Advertencia'),
        ('critico',     'Crítico'),
    ]
    ESTADO_CHOICES = [
        ('activa',   'Activa'),
        ('resuelta', 'Resuelta'),
        ('ignorada', 'Ignorada'),
    ]
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='alertas')
    dato_sensor = models.ForeignKey(DatoSensor, on_delete=models.SET_NULL, null=True, blank=True, related_name='alertas')
    mensaje     = models.TextField()
    nivel       = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='info')
    estado      = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    creada_en   = models.DateTimeField(auto_now_add=True)
    resuelta_en = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-creada_en']

    def __str__(self):
        return f"[{self.nivel.upper()}] {self.dispositivo.nombre}: {self.mensaje[:60]}"