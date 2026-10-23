from app.safety_rules import evaluate_safety_rules


def test_flame_alone_does_not_escalate_directly_to_fire():
    reading = {"temperature": 24, "humidity": 70, "smoke": 5, "gas": 0, "flame": True}
    probabilities = {"NORMAL": 0.15, "WARNING": 0.20, "FIRE": 0.65}
    result = evaluate_safety_rules(reading, probabilities, "FIRE")
    assert result["risk_level"] == "WARNING"


def test_fire_requires_corroborating_measurements():
    reading = {"temperature": 48, "humidity": 10, "smoke": 320, "gas": 150, "flame": True}
    probabilities = {"NORMAL": 0.01, "WARNING": 0.04, "FIRE": 0.95}
    result = evaluate_safety_rules(reading, probabilities, "FIRE")
    assert result["risk_level"] == "FIRE"
    assert result["rule"] == "FIRE_CORROBORATED"
