#!/usr/bin/env python3
"""
ejemplos_prueba.py
──────────────────
Formas de probar los endpoints del backend Django.
Ejecuta el servidor antes: python manage.py runserver
"""

# ═══════════════════════════════════════════════════════════
# OPCIÓN A: con la librería `requests` de Python
# pip install requests
# ═══════════════════════════════════════════════════════════

import requests
import json

BASE_URL = "http://localhost:8000/api"


def demo_requests():
    print("=" * 55)
    print("PRUEBAS CON requests (Python)")
    print("=" * 55)

    # ── 1. POST /api/datos/ ─ registrar lectura de sensor ──
    print("\n[1] POST /api/datos/ → registrar lectura")
    payload = {
        "dispositivo_id": 1,
        "valor": 23.5,
        "unidad": "°C",
        "metadata": {"bateria": 87, "señal": "fuerte"}
    }
    r = requests.post(f"{BASE_URL}/datos/", json=payload)
    print(f"  Status: {r.status_code}")
    print(f"  Respuesta: {json.dumps(r.json(), indent=2, ensure_ascii=False)}")

    # ── 2. POST con temperatura crítica (genera alerta automática) ──
    print("\n[2] POST /api/datos/ → temperatura crítica (> 40°C)")
    payload_critico = {
        "dispositivo_id": 1,
        "valor": 45.2,
        "unidad": "°C"
    }
    r = requests.post(f"{BASE_URL}/datos/", json=payload_critico)
    print(f"  Status: {r.status_code}")
    print(f"  Respuesta: {json.dumps(r.json(), indent=2, ensure_ascii=False)}")

    # ── 3. GET /api/datos/ ─ listar lecturas ──────────────────
    print("\n[3] GET /api/datos/ → listar últimas lecturas")
    r = requests.get(f"{BASE_URL}/datos/")
    print(f"  Status: {r.status_code}")
    data = r.json()
    print(f"  Total registros: {data.get('total')}")
    print(f"  Primeros 2: {json.dumps(data.get('datos', [])[:2], indent=2, ensure_ascii=False)}")

    # ── 4. GET /api/datos/ con filtros ───────────────────────
    print("\n[4] GET /api/datos/?dispositivo_id=1&limite=5")
    r = requests.get(f"{BASE_URL}/datos/", params={"dispositivo_id": 1, "limite": 5})
    print(f"  Status: {r.status_code}")
    print(f"  Datos: {len(r.json().get('datos', []))} registros")

    # ── 5. GET /api/alertas/ ─ listar alertas ────────────────
    print("\n[5] GET /api/alertas/ → listar alertas")
    r = requests.get(f"{BASE_URL}/alertas/")
    print(f"  Status: {r.status_code}")
    data = r.json()
    print(f"  Total alertas: {data.get('total')}")

    # ── 6. GET /api/alertas/ con filtro por nivel ────────────
    print("\n[6] GET /api/alertas/?nivel=critico")
    r = requests.get(f"{BASE_URL}/alertas/", params={"nivel": "critico"})
    print(f"  Status: {r.status_code}")
    print(f"  Alertas críticas: {r.json().get('total')}")

    print("\n✅ Pruebas completadas")


if __name__ == "__main__":
    demo_requests()


# ═══════════════════════════════════════════════════════════
# OPCIÓN B: con cURL (pegar en terminal)
# ═══════════════════════════════════════════════════════════
"""
# ── POST: registrar lectura de sensor ──────────────────────
curl -X POST http://localhost:8000/api/datos/ \
  -H "Content-Type: application/json" \
  -d '{
    "dispositivo_id": 1,
    "valor": 23.5,
    "unidad": "°C",
    "metadata": {"bateria": 87}
  }'

# ── POST: temperatura crítica (dispara alerta automática) ──
curl -X POST http://localhost:8000/api/datos/ \
  -H "Content-Type: application/json" \
  -d '{"dispositivo_id": 1, "valor": 45.2, "unidad": "°C"}'

# ── GET: listar lecturas ────────────────────────────────────
curl http://localhost:8000/api/datos/

# ── GET: listar lecturas con filtros ───────────────────────
curl "http://localhost:8000/api/datos/?dispositivo_id=1&limite=10&pagina=1"

# ── GET: listar alertas ────────────────────────────────────
curl http://localhost:8000/api/alertas/

# ── GET: alertas críticas activas ─────────────────────────
curl "http://localhost:8000/api/alertas/?nivel=critico&estado=activa"
"""


# ═══════════════════════════════════════════════════════════
# DATOS DE PRUEBA: cargar en Django shell
# python manage.py shell < seed.py
# ═══════════════════════════════════════════════════════════
"""
from nombre_de_tu_app.models import Usuario, Dispositivo, DatoSensor, Alerta

# Crear usuario admin
user = Usuario.objects.create_superuser(
    username='admin',
    password='admin123',
    email='admin@ejemplo.com',
    rol='admin'
)

# Crear dispositivo
sensor = Dispositivo.objects.create(
    nombre='Sensor Sala Principal',
    tipo='temperatura',
    ubicacion='Edificio A, Piso 2',
    activo=True,
    propietario=user
)

# Crear lecturas de ejemplo
for valor in [21.0, 22.5, 23.1, 38.0, 41.5]:
    DatoSensor.objects.create(
        dispositivo=sensor,
        valor=valor,
        unidad='°C'
    )

print(f"✅ {DatoSensor.objects.count()} lecturas creadas")
"""
