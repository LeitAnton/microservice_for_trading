import os

import motor.motor_asyncio

MONGO_INITDB_DATABASE = os.getenv('MONGO_INITDB_DATABASE')
MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_INITDB_PORT = os.getenv('MONGO_INITDB_PORT')
MONGO_INITDB_HOST = os.getenv('MONGO_INITDB_HOST')

MONGO_URI = (f"{MONGO_INITDB_DATABASE}://"
             + f"{MONGO_INITDB_ROOT_USERNAME}:"
             + f"{MONGO_INITDB_ROOT_PASSWORD}"
             + f"@{MONGO_INITDB_DATABASE}:{MONGO_INITDB_PORT}")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You have successfully connected to MongoDB!")
except Exception as e:
    print(e)

database = client.currencies

currencies_collection = database.get_collection("currencies_collection")
