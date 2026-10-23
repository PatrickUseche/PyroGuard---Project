# Integración de PyroGuard-IA con PyroGuard-Backend

## Qué se observó en el backend público

La versión revisada del backend usa Django REST Framework y actualmente recibe/lista mediciones con `POST/GET /api/readings/`. El modelo y serializer visibles contemplan `temperature`, `humidity`, `smoke`, `flame` y `timestamp`, pero no `gas` ni campos de predicción. El contrato del documento Forest Guardian contempla `gas` opcional y exige trazabilidad de la predicción.

Los archivos de esta carpeta son una referencia de integración para la versión revisada el 13 de octubre de 2026. Antes de reemplazar archivos, revisa si tus compañeros ya añadieron cambios posteriores y fusiona esos cambios; no sobrescribas trabajo nuevo sin revisarlo.

## Arquitectura

`ESP32/simulador -> Django POST /api/readings/ -> guarda la medición -> PyroGuard-IA POST /predict -> Django guarda riesgo -> Angular consulta GET /api/readings/`

La medición se guarda aunque el servicio IA no responda. En ese caso la respuesta incluye `prediction.status = unavailable` para no bloquear la recepción del ESP32.

## Pasos para integrar

1. Despliega el servicio de este repositorio (o levántalo localmente) y comprueba `GET /health`.
2. En el repositorio `PyroGuard-Backend`, fusiona los cambios de `models.py`, `serializers.py` y `views.py` de esta carpeta con la app `api/`. Mantén cualquier cambio de tus compañeros que no esté en estas versiones.
3. Añade `requests==2.32.5` a `requirements.txt` del backend.
4. Configura variables de entorno del backend:
   - `AI_SERVICE_URL=http://127.0.0.1:8001` si ambos servicios corren localmente en la misma máquina.
   - `AI_SERVICE_URL=https://TU-SERVICIO-IA.onrender.com` cuando esté desplegada la API IA; sin barra final.
   - `AI_SERVICE_TIMEOUT=2.5`
   - `AI_API_KEY=...` solo si configuraste una clave equivalente en el servicio IA.
5. Desde la raíz del backend, ejecuta:
   ```bash
   python manage.py makemigrations api
   python manage.py migrate
   ```
   Esto crea la migración para `gas` y los campos de resultado IA. No inventes ni edites manualmente el número de migración: deja que Django lo calcule sobre el estado real del repositorio.
6. Reinicia Django y crea un nodo con `node_id=NODE-001` en Django Admin (o usa un ID que exista). El serializer existente asocia las lecturas a un nodo ya registrado.
7. Envía una medición a `/api/readings/`. La respuesta debe incluir `measurement.risk_level`, `measurement.risk_probability`, `measurement.risk_probabilities` y `prediction`.
8. Haz `GET /api/readings/`; cada medición debe mostrar la clasificación guardada.

## Ejemplo local de prueba

Con IA en `http://127.0.0.1:8001` y backend en `http://127.0.0.1:8000`, registra antes el nodo `NODE-001`, y luego ejecuta:

```bash
curl -X POST http://127.0.0.1:8000/api/readings/ ^
  -H "Content-Type: application/json" ^
  -d "{\"node_id\":\"NODE-001\",\"temperature\":48,\"humidity\":10,\"smoke\":320,\"gas\":150,\"flame\":true,\"timestamp\":\"2026-10-13T22:00:00-05:00\"}"
```

PowerShell puede usar `Invoke-RestMethod`; adapta el comando a tu terminal.

## Importante sobre las limitaciones

- `gas` es opcional en el contrato y, si falta, el backend lo guarda como `0.0`.
- El modelo actual se entrena únicamente con datos sintéticos. Las métricas miden ese escenario sintético, no incendios reales.
- Los umbrales de las reglas son umbrales iniciales de prototipo: el equipo/docente debe aprobarlos y deben validarse con datos reales en condiciones seguras.
- La integración guarda los resultados en `SensorReading` para mantener trazabilidad básica. Si el equipo necesita historial independiente de predicciones, el siguiente paso es crear un modelo `Prediction` separado.
- Este cambio no crea por sí solo una tabla de alertas ni envía notificaciones; el backend debe consumir `risk_level == FIRE` para cumplir RF09.
