from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

RiskLevel = Literal["NORMAL", "WARNING", "FIRE"]


class SensorReadingInput(BaseModel):
    """Entrada alineada con el contrato del proyecto Forest Guardian."""
    model_config = ConfigDict(extra="ignore")

    node_id: str = Field(..., min_length=1, max_length=50, description="Identificador del nodo ESP32")
    temperature: float = Field(..., ge=-40, le=100, description="Temperatura en grados Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humedad relativa porcentual")
    smoke: float = Field(..., ge=0, le=10000, description="Lectura del sensor de humo")
    gas: float = Field(default=0.0, ge=0, le=10000, description="Lectura opcional del sensor de gases")
    flame: bool = Field(..., description="Detección del sensor de llama")
    timestamp: datetime | None = Field(default=None, description="Fecha/hora ISO 8601 de la medición")


class SafetyDecision(BaseModel):
    rule: str
    explanation: str
    fire_confirmations: list[str]
    warning_signals: list[str]


class PredictionResponse(BaseModel):
    status: Literal["ok"] = "ok"
    node_id: str
    timestamp: datetime
    model_version: str
    model_prediction: RiskLevel
    risk_level: RiskLevel
    # Probabilidad estimada de pertenecer a WARNING o FIRE; rango 0.0 a 1.0.
    risk_probability: float = Field(..., ge=0, le=1)
    risk_probability_percent: float = Field(..., ge=0, le=100)
    probabilities: dict[str, float]
    safety_rules: SafetyDecision
    synthetic_model: bool = True
    disclaimer: str


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    model_loaded: bool
    model_version: str | None = None
    classes: list[str] = []
