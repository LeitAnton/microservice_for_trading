import json
import ssl
import websockets

from database import currencies_collection
from producer.kafka_producer import send_message_to_kafka
from schemas.actions import Unsubscribe, Subscribe
from serializers.actions import subscribe_serializer, unsubscribe_serializer
from schemas.currency import Currency

websocket_messages = []


async def connect_to_external_websocket():
    from consumer.kafka_consumer import disposable_consumer
    topic_get_currencies = 'topic_get_currencies'
    data = await disposable_consumer(topic_get_currencies)
    subscribe = Subscribe(symbols=data['symbols'])

    async with (websockets.connect('wss://ws-feed.exchange.coinbase.com',
                                   ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)) as websocket):
        try:
            await subscribe_websocket(subscribe)

            while True:
                while websocket_messages:
                    message = websocket_messages.pop()
                    await websocket.send(message)

                response = await websocket.recv()
                response_data = json.loads(response)
                if response_data['type'] == 'ticker':
                    currency = Currency(
                        symbol=response_data['product_id'],
                        price=response_data['price']
                    )
                    await currencies_collection.insert_one(currency.dict())

                    topic_websocket_data = 'topic_websocket_data'
                    aim_currency = currency.symbol.split('-')[0]
                    message = {
                        'symbol': aim_currency,
                        'price': currency.price,
                    }
                    await send_message_to_kafka(topic_websocket_data, message)

        except websockets.exceptions.ConnectionClosed:
            await connect_to_external_websocket()


async def subscribe_websocket(subscribe: Subscribe):
    action = await subscribe_serializer(subscribe)
    serializer_action = json.dumps(action)
    websocket_messages.append(serializer_action)


async def unsubscribe_websocket(unsubscribe: Unsubscribe):
    action = await unsubscribe_serializer(unsubscribe)
    serializer_action = json.dumps(action)
    websocket_messages.append(serializer_action)
