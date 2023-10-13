import asyncio
import os
import json
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError


async def send_message_to_kafka(topic, message):
    kafka_url = os.environ.get('KAFKA_URL')

    producer = AIOKafkaProducer(
        loop=asyncio.get_event_loop(),
        bootstrap_servers=kafka_url,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    await producer.start()
    try:

        await producer.send_and_wait(topic, message)
    except KafkaConnectionError as e:
        print(f'Kafka Connection Error: {e}')
    finally:
        await producer.stop()
