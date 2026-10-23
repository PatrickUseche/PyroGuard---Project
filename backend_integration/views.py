"""Referencia integrada para api/views.py: guarda medición aunque la IA no esté disponible."""
import logging
import os
import requests
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SensorReadingSerializer
from .models import SensorReading

logger = logging.getLogger(__name__)


def call_ai_service(reading: SensorReading) -> dict:
    base_url = os.getenv("AI_SERVICE_URL", "").strip().rstrip("/")
    if not base_url:
        return {"status": "unavailable", "message": "AI_SERVICE_URL no está configurada."}

    payload = {
        "node_id": reading.node.node_id,
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "smoke": reading.smoke,
        "gas": reading.gas,
        "flame": reading.flame,
        "timestamp": reading.timestamp.isoformat(),
    }
    headers = {}
    api_key = os.getenv("AI_API_KEY", "").strip()
    if api_key:
        headers["X-AI-API-Key"] = api_key
    timeout = float(os.getenv("AI_SERVICE_TIMEOUT", "2.5"))

    response = requests.post(f"{base_url}/predict", json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    result = response.json()

    reading.risk_level = result["risk_level"]
    reading.risk_probability = float(result["risk_probability"])
    reading.risk_probabilities = result.get("probabilities", {})
    reading.model_version = result.get("model_version", "")
    reading.prediction_updated_at = timezone.now()
    reading.save(update_fields=[
        "risk_level", "risk_probability", "risk_probabilities", "model_version", "prediction_updated_at"
    ])
    return result


class ReceiveMeasurementView(APIView):
    def post(self, request):
        serializer = SensorReadingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        reading = serializer.save()
        try:
            prediction = call_ai_service(reading)
        except (requests.RequestException, ValueError, KeyError, TypeError) as error:
            logger.warning("La medición %s se guardó, pero no se pudo consultar la IA: %s", reading.pk, error)
            prediction = {
                "status": "unavailable",
                "risk_level": "UNKNOWN",
                "message": "La medición se guardó, pero el servicio de IA no respondió. Reintentar la predicción.",
            }

        reading.refresh_from_db()
        return Response(
            {
                "status": "success",
                "message": "Medición registrada correctamente.",
                "measurement": SensorReadingSerializer(reading).data,
                "prediction": prediction,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        latest_readings = SensorReading.objects.select_related("node").all().order_by("-timestamp")[:20]
        serializer = SensorReadingSerializer(latest_readings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
