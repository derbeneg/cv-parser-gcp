import base64
import json
import logging

def subscriber(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic."""
    data = base64.b64decode(event['data']).decode('utf-8')
    parsed = json.loads(data)
    logging.info(f"Received parsed CV data: {parsed}")
    # Here you could send an email, write to a log table, etc.
