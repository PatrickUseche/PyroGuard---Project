"""Prueba una predicción usando el modelo entrenado de PyroGuard."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent / "models" / "modelo_riesgo.pkl"
FEATURES = ["temperature", "humidity", "smoke", "gas", "flame"]


def read_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Valor inválido. Escribe un número.")


def read_int_binary(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value in {"0", "1"}:
            return int(value)
        print("Escribe 0 para no detectar llama o 1 para detectar llama.")


def main() -> None:
    print("=== PyroGuard | Predicción de riesgo ===")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "No existe el modelo. Ejecuta primero: python ai/2_entrenar_modelo.py"
        )

    model = joblib.load(MODEL_PATH)

    temperature = read_float("Temperatura (°C): ")
    humidity = read_float("Humedad (%): ")
    smoke = read_float("Humo: ")
    gas = read_float("Gas: ")
    flame = read_int_binary("Llama detectada (0/1): ")

    sample = pd.DataFrame(
        [[temperature, humidity, smoke, gas, flame]],
        columns=FEATURES,
    )

    prediction = model.predict(sample)[0]
    probabilities = model.predict_proba(sample)[0]
    probability_map = dict(zip(model.classes_, probabilities))

    print("\n==============================")
    print(f"Predicción: {prediction}")
    print("Probabilidades:")
    for label in ["NORMAL", "WARNING", "FIRE"]:
        probability = probability_map.get(label, 0.0)
        print(f"- {label}: {probability * 100:.2f}%")
    print("==============================")
    print("\nLa predicción es una estimación del prototipo y debe combinarse con las reglas de seguridad del sistema.")


if __name__ == "__main__":
    main()
