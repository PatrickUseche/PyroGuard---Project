"""Entrena y exporta el modelo Random Forest de PyroGuard."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "dataset_simulado.csv"
MODEL_PATH = BASE_DIR / "models" / "modelo_riesgo.pkl"

FEATURES = ["temperature", "humidity", "smoke", "gas", "flame"]
TARGET = "label"


def main() -> None:
    print("=== PyroGuard | Entrenamiento del modelo ===")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "No existe el dataset. Ejecuta primero: python ai/1_generar_dataset.py"
        )

    df = pd.read_csv(DATA_PATH)

    missing_columns = [column for column in FEATURES + [TARGET] if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Faltan columnas en el dataset: {missing_columns}")

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Datos de entrenamiento: {len(X_train)}")
    print(f"Datos de prueba: {len(X_test)}")
    print(f"Clases aprendidas: {list(model.classes_)}")
    print("\nImportancia de variables:")

    importances = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)
    for feature, importance in importances.items():
        print(f"- {feature}: {importance:.4f}")

    print(f"\nModelo guardado correctamente en: {MODEL_PATH}")
    print("El archivo .pkl es el modelo entrenado que posteriormente podrá cargar el backend.")


if __name__ == "__main__":
    main()
