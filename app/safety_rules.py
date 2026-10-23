"""Reglas de seguridad del prototipo (umbrales iniciales, no certificados)."""
from typing import Any


def evaluate_safety_rules(reading: dict[str, Any], probabilities: dict[str, float], model_prediction: str) -> dict[str, Any]:
    temperature = float(reading["temperature"])
    humidity = float(reading["humidity"])
    smoke = float(reading["smoke"])
    gas = float(reading.get("gas", 0.0) or 0.0)
    flame = bool(reading["flame"])

    fire_confirmations = []
    if flame and smoke >= 80:
        fire_confirmations.append("sensor de llama activo junto con humo >= 80")
    if flame and temperature >= 35:
        fire_confirmations.append("sensor de llama activo junto con temperatura >= 35 °C")
    if flame and gas >= 40:
        fire_confirmations.append("sensor de llama activo junto con gas >= 40")

    independent_high_signals = []
    if temperature >= 42:
        independent_high_signals.append("temperatura >= 42 °C")
    if smoke >= 180:
        independent_high_signals.append("humo >= 180")
    if gas >= 100:
        independent_high_signals.append("gas >= 100")
    if humidity <= 15:
        independent_high_signals.append("humedad <= 15 %")

    fire_probability = float(probabilities.get("FIRE", 0.0))
    corroborated_high_risk = len(independent_high_signals) >= 2 and fire_probability >= 0.55
    multiple_sensor_confirmation = len(independent_high_signals) >= 3 and smoke >= 120

    warning_signals = []
    if temperature >= 30:
        warning_signals.append("temperatura >= 30 °C")
    if humidity <= 35:
        warning_signals.append("humedad <= 35 %")
    if smoke >= 50:
        warning_signals.append("humo >= 50")
    if gas >= 30:
        warning_signals.append("gas >= 30")
    if flame:
        warning_signals.append("sensor de llama activo")

    # FIRE requiere señales corroboradas; una sola lectura extraña no crea una emergencia.
    if fire_confirmations or corroborated_high_risk or multiple_sensor_confirmation:
        return {
            "risk_level": "FIRE",
            "rule": "FIRE_CORROBORATED",
            "explanation": "Se detectaron varias señales concordantes de alto riesgo. Verificar la condición del entorno.",
            "fire_confirmations": fire_confirmations or independent_high_signals,
            "warning_signals": warning_signals,
        }

    # La llama aislada y una predicción fuerte sin corroboración elevan a WARNING, no a FIRE.
    model_risk = float(probabilities.get("WARNING", 0.0)) + fire_probability
    if flame or len(warning_signals) >= 2 or model_risk >= 0.55 or model_prediction == "WARNING":
        reasons = []
        if flame:
            reasons.append("la lectura de llama necesita corroboración con otros sensores")
        if len(warning_signals) >= 2:
            reasons.append("hay dos o más señales ambientales de advertencia")
        if model_risk >= 0.55:
            reasons.append("el modelo estima un riesgo ambiental elevado")
        explanation = "; ".join(reasons) if reasons else "El clasificador detectó una condición intermedia."
        return {
            "risk_level": "WARNING",
            "rule": "WARNING_REVIEW",
            "explanation": explanation,
            "fire_confirmations": [],
            "warning_signals": warning_signals,
        }

    return {
        "risk_level": "NORMAL",
        "rule": "NORMAL_BASELINE",
        "explanation": "No se alcanzaron los umbrales de advertencia definidos para este prototipo.",
        "fire_confirmations": [],
        "warning_signals": warning_signals,
    }
