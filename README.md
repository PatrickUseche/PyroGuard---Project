# PyroGuard-IA — Servicio de Machine Learning

Servicio de inferencia de IA para **PyroGuard / Forest Guardian**. Implementa un clasificador **Random Forest** entrenado localmente con un dataset sintético y lo expone mediante una API REST propia con FastAPI.

> **Alcance real:** es un prototipo académico reproducible. El dataset es sintético; no se debe presentar el modelo como detector certificado de incendios reales ni usarlo como único mecanismo de seguridad.

## Qué incluye

- Dataset simulado alineado con el contrato: `node_id`, `temperature`, `humidity`, `smoke`, `gas`, `flame`, `timestamp`, `label`.
- Entrenamiento Random Forest, partición estratificada 80/20 y métricas `accuracy`, `precision`, `recall`, `F1-score` y matriz de confusión.
- Artefacto versionado `models/modelo_riesgo.joblib` para que la API inicie sin entrenar en cada arranque.
- API REST con `GET /health`, `GET /` y `POST /predict`; documentación Swagger automática en `/docs`.
- Reglas de seguridad RF08 que combinan la salida del modelo con señales de sensores y no convierten una lectura aislada de llama en `FIRE`.
- Pruebas automatizadas, Dockerfile y configuración base para Render.
- Guía/archivos de referencia de integración con Django en `backend_integration/`.

## Requisitos

Python 3.11 o 3.12 recomendado. No requiere una API externa de OpenAI, Gemini u otro proveedor; Random Forest se ejecuta en el propio servicio.

## Inicio rápido en Windows

1. Descomprime este repositorio dentro de tu carpeta local de `PyroGuard-IA`.
2. Haz doble clic en `setup_windows.cmd`.
3. Ejecuta `start_windows.cmd`.
4. Abre `http://127.0.0.1:8001/docs`.

También puedes ejecutar manualmente desde esta raíz:

```bash
python -m venv .venv
# Windows CMD: .venv\Scripts\activate.bat
# PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

## API de predicción

`POST http://127.0.0.1:8001/predict`

Ejemplo de entrada compatible con el contrato del documento:

```json
{
  "node_id": "NODE-001",
  "temperature": 48,
  "humidity": 10,
  "smoke": 320,
  "gas": 150,
  "flame": true,
  "timestamp": "2026-10-13T22:00:00-05:00"
}
```

`gas` es opcional. Si el hardware no separa un sensor de gas, el servicio utiliza `0.0`; eso debe quedar documentado por el equipo. `node_id`, temperatura, humedad, humo y llama son obligatorios.

La respuesta incluye:

- `model_prediction`: clase elegida directamente por Random Forest.
- `probabilities`: probabilidades estimadas por clase (no necesariamente calibradas).
- `risk_probability`: suma `P(WARNING) + P(FIRE)`, expresada entre `0.0` y `1.0`.
- `risk_probability_percent`: la misma puntuación en porcentaje.
- `risk_level`: clasificación final tras las reglas de corroboración.
- `safety_rules`: regla usada y señales que motivaron la salida.
- `model_version`, `timestamp` y advertencia del alcance sintético.

Ejemplo de respuesta abreviada:

```json
{
  "status": "ok",
  "node_id": "NODE-001",
  "model_version": "pyroguard-rf-1.0.0",
  "model_prediction": "FIRE",
  "risk_level": "FIRE",
  "risk_probability": 0.98,
  "risk_probability_percent": 98.0,
  "probabilities": {"NORMAL": 0.01, "WARNING": 0.01, "FIRE": 0.98},
  "safety_rules": {
    "rule": "FIRE_CORROBORATED",
    "explanation": "...",
    "fire_confirmations": ["..."],
    "warning_signals": ["..."]
  },
  "synthetic_model": true,
  "disclaimer": "..."
}
```

Las probabilidades son ilustrativas; la respuesta concreta se calcula con el modelo incluido.

## Reentrenar

```bash
python scripts/1_generar_dataset.py
python scripts/2_entrenar_modelo.py
python -m pytest -q
```

El dataset tiene 2.400 filas sintéticas, 800 por clase. El script usa un split estratificado 80/20 y escribe el modelo, el reporte de clasificación y la matriz de confusión.

Para probar casos prediseñados:

```bash
python scripts/3_probar_predicciones.py
```

## Variables de entorno

Copia `.env.example` a `.env` si quieres documentar variables localmente (el código no carga `.env` automáticamente para la IA). Las variables deben definirse en el entorno del proceso o plataforma:

- `AI_API_KEY`: opcional. Si se configura, `POST /predict` requiere el header `X-AI-API-Key` con la misma clave.

La versión que devuelve la API se lee de los metadatos guardados dentro del artefacto entrenado, para conservar la trazabilidad del modelo.

En producción, define `AI_API_KEY` en la configuración de secretos del host; nunca subas una clave real al repositorio.

## Integración con Django

Consulta `backend_integration/INTEGRACION_BACKEND.md`. La integración propuesta hace que Django guarde la medición, solicite la predicción a esta API, persista el resultado en la misma medición y lo entregue por `GET /api/readings/`. Si la IA no responde, la medición se conserva y queda marcada sin predicción disponible.

Arquitectura:

```text
ESP32 / simulador
      ↓ JSON del contrato
PyroGuard-Backend (Django)
      ↓ POST /predict
PyroGuard-IA (FastAPI + Random Forest + reglas RF08)
      ↓ risk_level / probabilities / model_version
Django guarda la predicción
      ↓ GET /api/readings/
Angular Dashboard
```

## Relación con el documento de requisitos

- **RF06:** modelo entrenado que calcula clase y puntuación de riesgo, con versión documentada.
- **RF07:** clasificación `NORMAL`, `WARNING` o `FIRE` y probabilidades estimadas.
- **RF08:** reglas de corroboración que combinan IA y sensores; una lectura atípica aislada no marca por sí sola `FIRE`.
- **RF15:** dataset y casos de prueba sin ESP32 real.
- **RNF07/RNF08/RNF14:** versión del modelo, estructura modular, documentación y pruebas automatizadas.

## Despliegue

### Render

1. Crea un Web Service apuntando al repositorio `PyroGuard-IA`.
2. Usa `render.yaml` (o define Build Command `pip install -r requirements.txt`, Start Command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, Health Check Path `/health`).
3. Define una variable secreta `AI_API_KEY` si el servicio queda público.
4. Verifica `https://TU-SERVICIO.onrender.com/health` y la documentación en `/docs`.
5. Configura en el backend `AI_SERVICE_URL=https://TU-SERVICIO.onrender.com` y `AI_API_KEY` con el mismo valor secreto.

No escribas el dominio de ejemplo como si fuera real: usa la URL que la plataforma genere al desplegar.

## Limitaciones y trabajo pendiente

- Sustituir progresivamente el dataset sintético por datos reales, etiquetados y recogidos bajo supervisión segura.
- Revisar umbrales de RF08 con el docente y el equipo de hardware.
- Medir recall de FIRE, falsos negativos y falsos positivos en un conjunto separado que represente el entorno objetivo.
- Integrar persistencia/historial de predicciones y alertas en backend.
- Verificar contrato exacto del ESP32: escala real del sensor de humo/gas y codificación de `flame`.
