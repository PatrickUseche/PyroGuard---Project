"""Evalúa el Random Forest con métricas de clasificación."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "dataset_simulado.csv"
MODEL_PATH = BASE_DIR / "models" / "modelo_riesgo.pkl"
FEATURES = ["temperature", "humidity", "smoke", "gas", "flame"]
TARGET = "label"


def main() -> None:
    print("=== PyroGuard | Evaluación del modelo ===")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "No existe el dataset. Ejecuta primero: python ai/1_generar_dataset.py"
        )
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "No existe el modelo. Ejecuta primero: python ai/2_entrenar_modelo.py"
        )

    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES]
    y = df[TARGET]

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = joblib.load(MODEL_PATH)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy * 100:.2f}%\n")

    print("Reporte de clasificación:")
    print(classification_report(y_test, predictions, digits=3, zero_division=0))

    labels = list(model.classes_)
    matrix = confusion_matrix(y_test, predictions, labels=labels)
    matrix_df = pd.DataFrame(
        matrix,
        index=[f"Real_{label}" for label in labels],
        columns=[f"Pred_{label}" for label in labels],
    )

    print("Matriz de confusión:")
    print(matrix_df.to_string())

    print("\nNota: estas métricas corresponden a datos sintéticos de prueba y no representan rendimiento en incendios forestales reales.")


if __name__ == "__main__":
    main()
