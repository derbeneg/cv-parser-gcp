# api/worker/main.py
import os, json
from google.cloud import pubsub_v1

def main():
    project = os.environ["PROJECT_ID"]
    sub_name = os.environ["PUBSUB_SUBSCRIPTION"]
    client = pubsub_v1.SubscriberClient()
    sub_path = client.subscription_path(project, sub_name)

    def callback(msg):
        data = msg.data.decode()
        print("VM got message:", data)
        msg.ack()

    streaming = client.subscribe(sub_path, callback=callback)
    print("Worker listening…")
    streaming.result()
