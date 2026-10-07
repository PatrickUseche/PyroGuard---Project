# PyroGuard — Project | Avance de Inteligencia Artificial

## Descripción

Este módulo corresponde al avance del componente de Inteligencia Artificial del proyecto **PyroGuard**, sistema orientado al monitoreo y detección temprana de condiciones asociadas a incendios forestales.

El objetivo de este avance es demostrar un flujo funcional de Machine Learning **sin depender todavía del ESP32 ni de datos reales**:

1. Generar un dataset simulado.
2. Entrenar un clasificador Random Forest.
3. Evaluar el modelo mediante métricas de clasificación.
4. Exportar el modelo entrenado.
5. Probar predicciones con nuevos datos de sensores.

Los datos utilizados son sintéticos y están destinados exclusivamente a pruebas del prototipo.

## Relación con los requisitos del proyecto

Este avance trabaja principalmente los requisitos:

- **RF06 — Cálculo de riesgo mediante IA:** el modelo utiliza variables ambientales para estimar una categoría de riesgo.
- **RF07 — Clasificación del nivel de riesgo:** la salida se expresa como `NORMAL`, `WARNING` o `FIRE` y también se muestran probabilidades.
- **RF15 — Simulación de datos para pruebas:** se pueden generar escenarios simulados sin disponer del ESP32 conectado.

La integración posterior con backend, sensores y reglas de seguridad se realizará en fases siguientes.

## Contrato de datos utilizado

El dataset utiliza los campos definidos para las mediciones del proyecto:

| Campo | Descripción |
|---|---|
| `node_id` | Identificador del nodo ESP32 |
| `temperature` | Temperatura medida en °C |
| `humidity` | Humedad relativa |
| `smoke` | Lectura del sensor de humo/gases |
| `gas` | Lectura de gases |
| `flame` | Detección de llama (`0` o `1`) |
| `timestamp` | Fecha y hora de la medición |
| `label` | Categoría utilizada para entrenar la IA |

Las variables utilizadas como entrada del Random Forest son:

```text
temperature
humidity
smoke
gas
flame
```

## Estructura

```text
project/
├── ai/
│   ├── data/
│   │   └── dataset_simulado.csv      # generado localmente
│   ├── models/
│   │   └── modelo_riesgo.pkl         # generado localmente
│   ├── 1_generar_dataset.py
│   ├── 2_entrenar_modelo.py
│   ├── 3_evaluar_modelo.py
│   └── 4_predecir_riesgo.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalación

Se recomienda trabajar en un entorno virtual de Python.

```bash
python -m venv .venv
```

### Windows CMD

```cmd
.venv\Scripts\activate
pip install -r requirements.txt
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del repositorio:

### 1. Generar dataset

```bash
python ai/1_generar_dataset.py
```

Se crea:

```text
ai/data/dataset_simulado.csv
```

El dataset contiene 120 registros simulados distribuidos en los escenarios `NORMAL`, `WARNING` y `FIRE`.

### 2. Entrenar el modelo

```bash
python ai/2_entrenar_modelo.py
```

Se crea:

```text
ai/models/modelo_riesgo.pkl
```

Este archivo contiene el clasificador Random Forest entrenado y serializado.

### 3. Evaluar el modelo

```bash
python ai/3_evaluar_modelo.py
```

La consola muestra:

- Accuracy.
- Precision, recall y F1-score por clase.
- Matriz de confusión.

### 4. Probar una predicción

```bash
python ai/4_predecir_riesgo.py
```

El programa solicita valores de temperatura, humedad, humo, gas y llama, y devuelve la clasificación y las probabilidades para `NORMAL`, `WARNING` y `FIRE`.

## Flujo de la IA

```text
Sensores / datos simulados
          ↓
   Variables ambientales
          ↓
     Random Forest
          ↓
  Probabilidad por clase
          ↓
 NORMAL / WARNING / FIRE
          ↓
    Backend / Dashboard
```

## Consideraciones

El modelo se entrenó con datos sintéticos generados específicamente para el prototipo. Por lo tanto, un resultado alto de las métricas **no significa** que el modelo tenga el mismo desempeño con datos de incendios reales.

La IA no sustituye a los sensores ni debe presentarse como un detector certificado. La arquitectura del proyecto contempla posteriormente combinar la predicción con reglas de seguridad antes de generar una condición de alerta.

## Integración futura

La fase siguiente contempla:

- Integrar el modelo exportado con el backend.
- Recibir datos del ESP32 mediante el mecanismo definido por el equipo.
- Aplicar reglas de seguridad junto con la predicción de IA.
- Registrar la predicción asociada al nodo y a la medición.
- Exponer la predicción al dashboard.

## Evidencia sugerida para la presentación

Para demostrar este avance se recomienda mostrar en la terminal:

```text
1. Generación de dataset correcta.
2. Entrenamiento del Random Forest.
3. Métricas de evaluación.
4. Creación de modelo_riesgo.pkl.
5. Una predicción de ejemplo NORMAL, WARNING y FIRE.
```
