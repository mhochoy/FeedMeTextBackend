import uuid
import routes.texts
import fastapi.exceptions
import pymongo.errors

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from crud.models import user
from crud.models import text

router = APIRouter()


@router.get('/users', response_model=user.UserCollection, response_model_by_alias=False, description="Get all creators")
async def get_all_creators(request: Request):
    creators_obj = request.app.database["users"].find(limit=100)
    creators = await creators_obj.to_list(length=100)
    if creators:
        return user.UserCollection(users=creators)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No texts found!")


@router.get('/texts', response_model=text.TextCollection, response_model_by_alias=False, description="Get all texts")
async def get_all_texts(request: Request):
    texts_obj = request.app.database["texts"].find(limit=100)
    texts = await texts_obj.to_list(length=100)
    if texts:
        return text.TextCollection(texts=texts)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No texts found!")
