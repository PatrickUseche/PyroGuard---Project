"""Genera un dataset simulado para entrenar el modelo de riesgo de PyroGuard.

El dataset sigue el contrato de datos definido para el proyecto:
node_id, temperature, humidity, smoke, gas, flame y timestamp.
La columna adicional `label` representa la categoría que aprenderá el modelo.

IMPORTANTE: los datos son sintéticos y sirven únicamente para pruebas del prototipo.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

SEED = 42
SAMPLES_PER_CLASS = 40
OUTPUT_PATH = Path(__file__).resolve().parent / "data" / "dataset_simulado.csv"


def generate_sample(label: str, node_id: str, timestamp: str) -> list[object]:
    """Genera una medición sintética según el escenario indicado."""
    # Se dejan algunos rangos de solapamiento para que el problema no sea
    # completamente trivial para el clasificador.
    if label == "NORMAL":
        temperature = random.uniform(15.0, 29.0)
        humidity = random.uniform(45.0, 80.0)
        smoke = random.randint(0, 45)
        gas = random.randint(0, 20)
        flame = 0 if random.random() < 0.98 else 1

    elif label == "WARNING":
        temperature = random.uniform(27.0, 38.0)
        humidity = random.uniform(18.0, 45.0)
        smoke = random.randint(35, 170)
        gas = random.randint(15, 90)
        flame = 1 if random.random() < 0.08 else 0

    elif label == "FIRE":
        temperature = random.uniform(34.0, 55.0)
        humidity = random.uniform(5.0, 23.0)
        smoke = random.randint(160, 800)
        gas = random.randint(80, 400)
        flame = 1 if random.random() < 0.92 else 0

    else:
        raise ValueError(f"Etiqueta no válida: {label}")

    return [
        node_id,
        round(temperature, 2),
        round(humidity, 2),
        smoke,
        gas,
        flame,
        timestamp,
        label,
    ]


def main() -> None:
    print("=== PyroGuard | Generación de dataset ===")
    print(f"Semilla aleatoria: {SEED}")

    random.seed(SEED)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    base_time = datetime(2026, 10, 6, 18, 30, tzinfo=timezone(timedelta(hours=-5)))
    rows: list[list[object]] = []

    labels = ["NORMAL", "WARNING", "FIRE"]
    index = 0

    for label in labels:
        for _ in range(SAMPLES_PER_CLASS):
            node_id = f"NODE-{(index % 5) + 1:03d}"
            timestamp = (base_time + timedelta(minutes=index)).isoformat()
            rows.append(generate_sample(label, node_id, timestamp))
            index += 1

    random.shuffle(rows)

    columns = [
        "node_id",
        "temperature",
        "humidity",
        "smoke",
        "gas",
        "flame",
        "timestamp",
        "label",
    ]
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Dataset creado: {OUTPUT_PATH}")
    print(f"Registros: {len(df)}")
    print("Distribución de clases:")
    print(df["label"].value_counts().sort_index())
    print("\nPrimeras 5 filas:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
