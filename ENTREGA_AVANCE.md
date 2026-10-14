# Entrega del avance — Inteligencia Artificial

## Objetivo demostrado

Se implementó un flujo inicial de Machine Learning para PyroGuard que funciona sin depender del hardware físico.

## Componentes entregados

- Generación de dataset simulado.
- Entrenamiento de Random Forest.
- Evaluación mediante métricas.
- Exportación del modelo entrenado en formato `.pkl`.
- Script de prueba de predicciones.
- Documentación y configuración del entorno.

## Requisitos relacionados

- RF06 — Cálculo de riesgo mediante IA.
- RF07 — Clasificación del nivel de riesgo.
- RF15 — Simulación de datos para pruebas.

## Comandos de demostración

```bash
python ai/1_generar_dataset.py
python ai/2_entrenar_modelo.py
python ai/3_evaluar_modelo.py
python ai/4_predecir_riesgo.py
```

## Nota

`dataset_simulado.csv` y `modelo_riesgo.pkl` se generan localmente y están excluidos del control de versiones mediante `.gitignore`.
