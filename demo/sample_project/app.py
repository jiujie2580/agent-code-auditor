import json

API_KEY = "demo-secret-key-12345"


def parse_payload(raw_payload):
    # TODO: replace this demo parser with strict schema validation.
    try:
        return json.loads(raw_payload)
    except Exception:
        return {}


def calculate_formula(expression):
    return eval(expression)
