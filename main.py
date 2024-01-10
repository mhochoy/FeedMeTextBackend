import app as mongo
from routes.texts import router as text_router
from routes.users import router as user_router
from routes.audit import router as audit_router
from fastapi import FastAPI


app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = mongo.get_client()
    app.database = app.mongodb_client.test
    print("Connected to the database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get('/')
async def root():
    return {"message": "Welcome to the PyMongo tutorial!"}


app.include_router(text_router, tags=["texts"], prefix="/t")
app.include_router(user_router, tags=["users"], prefix='/u')
app.include_router(audit_router, tags=["audit"], prefix='/audit')


def query(texts_db):
    text_details = texts_db.find()
    for detail in text_details:
        print(detail['creator']+f'@{detail["date"]}: ', detail['message'])


def index(texts_db):
    texts_db.create_index("creator")


# if __name__ == '__main__':
#     dbname = mongo.get_database()
#
#     db_texts = dbname["texts"]
#     db_texts.insert_many(
#         [text_1,
#          text_2,
#          text_3,
#          text_4,
#          text_5]
#     )
#
#     index(db_texts)
#     query(db_texts)
