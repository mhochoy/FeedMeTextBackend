import os

from dotenv import dotenv_values


def get_uri():
    config = os.environ['MONGO_URI']

    return config


def get_db():
    db = os.environ['MONGO_TEST_DB']

    return db
