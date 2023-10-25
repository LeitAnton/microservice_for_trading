import asyncio
import json
import os
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from websocket_connection.websocket import subscribe_websocket, unsubscribe_websocket
from schemas.actions import Subscribe, Unsubscribe

kafka_url = os.environ.get('KAFKA_URL')


async def constant_consumer():
    topic_currency_action = 'topic_currency_action'
    consumer = AIOKafkaConsumer(
        topic_currency_action,
        loop=asyncio.get_event_loop(),
        bootstrap_servers=kafka_url,
    )

    try:
        await consumer.start()
        async for message in consumer:
            data = message.value
            decode_data = json.loads(data)

            if decode_data['action'] == 'unsubscribe':
                unsubscribe = Unsubscribe(symbols=[decode_data['symbol']])
                await unsubscribe_websocket(unsubscribe)

            if decode_data['action'] == 'subscribe':
                subscribe = Subscribe(symbols=[decode_data['symbol']])
                await subscribe_websocket(subscribe)

    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer.stop()
    await constant_consumer()


async def disposable_consumer(topic):
    consumer = AIOKafkaConsumer(
        topic,
        loop=asyncio.get_event_loop(),
        bootstrap_servers=kafka_url,
    )
    decode_data = None

    try:
        await consumer.start()
        message = await consumer.getone()
        decode_data = json.loads(message.value)
    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer.stop()
    return decode_data
