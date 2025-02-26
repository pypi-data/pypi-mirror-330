from confluent_kafka import Producer
from .setup import read_config

config = read_config


def acked(err, msg):
    # NB needs to be updated and logged.
    if err is not None:
        print(f"Failed to deliver message: {err.str()}")
    else:
        print(f"Message published successfully")


def publish_message(topic, value, key):
    producer = Producer(**config)  # NB needs to moved
    producer.produce(topic, key=key, value=value, callback=acked)
    producer.flush()  # NB needs to moved
    return "Message published"
