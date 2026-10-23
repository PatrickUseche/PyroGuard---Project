"""Referencia integrada para api/serializers.py del backend."""
from rest_framework import serializers
from .models import Node, SensorReading


class SensorReadingSerializer(serializers.ModelSerializer):
    node_id = serializers.SlugRelatedField(
        queryset=Node.objects.all(),
        slug_field="node_id",
        source="node",
    )
    gas = serializers.FloatField(required=False, default=0.0)

    class Meta:
        model = SensorReading
        fields = [
            "id",
            "node_id",
            "temperature",
            "humidity",
            "smoke",
            "gas",
            "flame",
            "timestamp",
            "risk_level",
            "risk_probability",
            "risk_probabilities",
            "model_version",
            "prediction_updated_at",
        ]
        read_only_fields = [
            "id",
            "risk_level",
            "risk_probability",
            "risk_probabilities",
            "model_version",
            "prediction_updated_at",
        ]
