import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.models import Max
from django.db.models import Min

from .models import DatoSensor, Alerta, Dispositivo

UMBRALES = {
    'temperatura': {'advertencia': 35.0,  'critico': 40.0},   # °C
    'humedad':     {'advertencia': 80.0,  'critico': 95.0},   # %
    'sonido':      {'advertencia': 80.0,  'critico': 100.0},  # dB
    'luz':         {'advertencia': 800.0, 'critico': 1000.0}, # lux
}

tipos_validos = ['temperatura', 'humedad', 'sonido', 'luz']

def serializar_dispositivo(d):
    return {
        "id": d.id,
        "nombre": d.nombre,
        "activo": d.activo,
        "sensores": d.sensores_activos(),
    }

def serializar_dato(dato):
    return {
        "id": dato.id,
        "dispositivo_id": dato.dispositivo_id,
        "dispositivo_nombre": dato.dispositivo.nombre,
        "tipo_sensor": dato.tipo_sensor,
        "valor": dato.valor,
        "unidad": dato.unidad,
        "timestamp": dato.timestamp.isoformat(),
    }


def serializar_alerta(alerta):
    return {
        "id": alerta.id,
        "dispositivo_id": alerta.dispositivo_id,
        "dispositivo_nombre": alerta.dispositivo.nombre,
        "mensaje": alerta.mensaje,
        "nivel": alerta.nivel,
        "estado": alerta.estado,
        "creada_en": alerta.creada_en.isoformat(),
        "resuelta_en": alerta.resuelta_en.isoformat() if alerta.resuelta_en else None,
    }


def generar_alerta_si_aplica(dispositivo, dato):
    """Genera alerta automática según umbrales definidos."""
    umbral = UMBRALES.get(dato.tipo_sensor)
    if not umbral:
        return

    if dato.valor >= umbral['critico']:
        nivel = 'critico'
        mensaje = f"{dato.tipo_sensor.capitalize()} crítica: {dato.valor} {dato.unidad}"
    elif dato.valor >= umbral['advertencia']:
        nivel = 'advertencia'
        mensaje = f"{dato.tipo_sensor.capitalize()} elevada: {dato.valor} {dato.unidad}"
    else:
        return  # Valor normal, no se genera alerta

    Alerta.objects.create(
        dispositivo=dispositivo,
        dato_sensor=dato,
        mensaje=mensaje,
        nivel=nivel,
    )


# ─────────────────────────────────────────────
# GET/POST /api/datos/
# ─────────────────────────────────────────────
@method_decorator(csrf_exempt, name='dispatch')
class DatosView(View):

    def get(self, request):
        """
        Query params opcionales:
          - dispositivo_id (int)
          - tipo_sensor: temperatura | humedad | sonido | luz
          - limite (int, default 50)
          - pagina (int, default 1)
        """
        dispositivo_id = request.GET.get('dispositivo_id')
        tipo_sensor    = request.GET.get('tipo_sensor')
        limite         = int(request.GET.get('limite', 50))
        pagina         = int(request.GET.get('pagina', 1))

        qs = DatoSensor.objects.select_related('dispositivo').all()
        if dispositivo_id:
            qs = qs.filter(dispositivo_id=dispositivo_id)
        if tipo_sensor:
            qs = qs.filter(tipo_sensor=tipo_sensor)

        paginator = Paginator(qs, limite)
        page_obj  = paginator.get_page(pagina)

        return JsonResponse({
            "ok": True,
            "total": paginator.count,
            "paginas": paginator.num_pages,
            "pagina_actual": pagina,
            "datos": [serializar_dato(d) for d in page_obj.object_list],
        })

    def post(self, request):
        """
        Body JSON esperado:
        {
            "dispositivo_id": 1,
            "tipo_sensor": "temperatura",   ← temperatura | humedad | iluminacion | ruido
            "valor": 23.5,
            "unidad": "°C"
        }
        """
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)

        campos_requeridos = ['dispositivo_id', 'tipo_sensor', 'valor', 'unidad']
        faltantes = [c for c in campos_requeridos if c not in body]
        if faltantes:
            return JsonResponse({"ok": False, "error": f"Campos requeridos: {faltantes}"}, status=400)

        # Validar que el tipo_sensor sea válido
        tipos_validos = ['temperatura', 'humedad', 'sonido', 'luz']
        if body['tipo_sensor'] not in tipos_validos:
            return JsonResponse({"ok": False, "error": f"tipo_sensor debe ser uno de: {tipos_validos}"}, status=400)

        try:
            dispositivo = Dispositivo.objects.get(id=body['dispositivo_id'], activo=True)
        except Dispositivo.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Dispositivo no encontrado o inactivo"}, status=404)

        # Validar que el dispositivo tenga ese sensor
        if body['tipo_sensor'] not in dispositivo.sensores_activos():
            return JsonResponse({
                "ok": False,
                "error": f"El dispositivo no tiene sensor de {body['tipo_sensor']}. Sensores disponibles: {dispositivo.sensores_activos()}"
            }, status=400)

        dato = DatoSensor.objects.create(
            dispositivo=dispositivo,
            tipo_sensor=body['tipo_sensor'],
            valor=float(body['valor']),
            unidad=body['unidad'],
            metadata=body.get('metadata'),
        )

        generar_alerta_si_aplica(dispositivo, dato)

        return JsonResponse({"ok": True, "dato": serializar_dato(dato)}, status=201)


# ─────────────────────────────────────────────
# GET /api/alertas/
# ─────────────────────────────────────────────
@method_decorator(csrf_exempt, name='dispatch')
class AlertasView(View):

    def get(self, request):
        """
        Query params opcionales:
          - estado: activa | resuelta | ignorada
          - nivel:  info | advertencia | critico
          - dispositivo_id (int)
        """
        estado         = request.GET.get('estado')
        nivel          = request.GET.get('nivel')
        dispositivo_id = request.GET.get('dispositivo_id')

        qs = Alerta.objects.select_related('dispositivo').all()
        if estado:         qs = qs.filter(estado=estado)
        if nivel:          qs = qs.filter(nivel=nivel)
        if dispositivo_id: qs = qs.filter(dispositivo_id=dispositivo_id)

        alertas = [serializar_alerta(a) for a in qs[:100]]

        return JsonResponse({"ok": True, "total": len(alertas), "alertas": alertas})


# ─────────────────────────────────────────────
# GET /api/dispositivos/
# ─────────────────────────────────────────────
@method_decorator(csrf_exempt, name='dispatch')
class DispositivosView(View):

    def get(self, request):
        """Lista todos los dispositivos activos con sus sensores."""
        qs = Dispositivo.objects.filter(activo=True)
        return JsonResponse({
            "ok": True,
            "dispositivos": [serializar_dispositivo(d) for d in qs],
        })

# ─────────────────────────────────────────────
# GET /api/dashboard/
# ─────────────────────────────────────────────
@method_decorator(csrf_exempt, name='dispatch')
class DashboardView(View):

    def get(self, request):

        dispositivos = (
            Dispositivo.objects
            .filter(activo=True)
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
                }
                for alerta in dispositivo.alertas.all()[:10]
            ]

            resultado.append({
                "id": dispositivo.id,
                "nombre": dispositivo.nombre,
                "activo": dispositivo.activo,
                "sensores": dispositivo.sensores_activos(),
                "datos": datos,
                "alertas": alertas,
            })

        return JsonResponse({
            "ok": True,
            "total": len(resultado),
            "dispositivos": resultado
        })
    
class HistorialView(View):

    def get(self, request):

        datos = DatoSensor.objects.select_related(
            'dispositivo'
        ).all().order_by('-timestamp')

        historial = [

            {
                "id": dato.id,

                "sensor": dato.tipo_sensor,

                "valor": dato.valor,

                "unidad": dato.unidad,

                "fecha": dato.timestamp.isoformat(),

                "dispositivo": {
                    "nombre": dato.dispositivo.nombre,
                    "ubicacion": dato.dispositivo.ubicacion,
                }

            }

            for dato in datos[:100]

        ]

        # =========================
        # PROMEDIOS
        # =========================

        promedio_temperatura = datos.filter(
            tipo_sensor='temperatura'
        ).aggregate(
            promedio=Avg('valor')
        )

        promedio_humedad = datos.filter(
            tipo_sensor='humedad'
        ).aggregate(
            promedio=Avg('valor')
        )

        promedio_sonido = datos.filter(
            tipo_sensor='sonido'
        ).aggregate(
            promedio=Avg('valor')
        )

        promedio_luz = datos.filter(
            tipo_sensor='luz'
        ).aggregate(
            promedio=Avg('valor')
        )

        # =========================
        # MÁXIMOS
        # =========================

        maximo = datos.aggregate(
            maximo=Max('valor')
        )

        # =========================
        # MÍNIMOS
        # =========================

        minimo = datos.aggregate(
            minimo=Min('valor')
        )

        return JsonResponse({

            "ok": True,

            "historial": historial,

            "estadisticas": {

                "promedios": {

                    "temperatura":
                        promedio_temperatura['promedio'],

                    "humedad":
                        promedio_humedad['promedio'],

                    "sonido":
                        promedio_sonido['promedio'],

                    "luz":
                        promedio_luz['promedio'],
                },

                "maximo":
                    maximo['maximo'],

                "minimo":
                    minimo['minimo'],
            }

        })