import asyncio
import os

from aiokafka import AIOKafkaClient
from fastapi import FastAPI

from consumer.kafka_consumer import constant_consumer
from routing.currency import router as currency_routing
from websocket_connection.websocket import connect_to_external_websocket


topic = 'topic_websocket_data'
kafka_url = os.environ.get('KAFKA_URL')

kafka_client = AIOKafkaClient(
    loop=asyncio.get_event_loop(),
    bootstrap_servers=kafka_url
)
kafka_client.add_topic(topic)

app = FastAPI(openapi_url="/core/openapi.json", docs_url="/core/docs")
app.include_router(currency_routing)


async def startup_tasks():
    tasks = [connect_to_external_websocket(), constant_consumer()]
    await asyncio.gather(*tasks)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(startup_tasks())
