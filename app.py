import asyncio
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from config import get_uri, get_db


def get_client():
    client = AsyncIOMotorClient(get_uri(), server_api=ServerApi('1'))

    return client


def get_database():
    db = get_db()

    return db
