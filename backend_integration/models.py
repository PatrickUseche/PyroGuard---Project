"""Referencia integrada para api/models.py del backend actual. Fusiona si ya hubo cambios nuevos."""
from django.db import models
from django.utils import timezone


class Node(models.Model):
    node_id = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_communication = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.node_id


class SensorReading(models.Model):
    RISK_CHOICES = [
        ("UNKNOWN", "Unknown"),
        ("NORMAL", "Normal"),
        ("WARNING", "Warning"),
        ("FIRE", "Fire"),
    ]

    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="readings")
    temperature = models.FloatField()
    humidity = models.FloatField()
    smoke = models.FloatField()
    # El contrato contempla gas opcional; si el nodo no tiene ese sensor se almacena 0.0.
    gas = models.FloatField(default=0.0)
    flame = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    # Resultado de IA guardado junto a la medición para trazabilidad (RNF07).
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default="UNKNOWN")
    risk_probability = models.FloatField(null=True, blank=True)  # rango 0.0 a 1.0
    risk_probabilities = models.JSONField(default=dict, blank=True)
    model_version = models.CharField(max_length=50, blank=True, default="")
    prediction_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.node.node_id} - {self.timestamp}"
