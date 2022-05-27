from kafka import KafkaProducer
from dotenv import load_dotenv
from json import dumps
import os

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_CLUSTER_URLS"),
    value_serializer=lambda x: dumps(x).encode("utf-8"),
    client_id="plugin.video",
)
