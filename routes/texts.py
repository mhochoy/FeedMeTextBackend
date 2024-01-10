import uuid
import fastapi.exceptions
import pymongo.errors

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from crud.models import text


router = APIRouter()


@router.post(
    '/',
    response_description="Create a text",
    status_code=status.HTTP_201_CREATED,
    response_model=text.Text,
    response_model_by_alias=False
)
async def create_text(request: Request, text: text.Text = Body(...)):
    try:
        text = jsonable_encoder(text)
        new_text = await request.app.database["texts"].insert_one(text)
        created_text = await request.app.database["texts"].find_one(
            {"_id": new_text.inserted_id}
        )

        return created_text
    except fastapi.exceptions.ResponseValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        print(e.msg)

    except pymongo.errors.DuplicateKeyError as d:
        text = jsonable_encoder(text)
        text["_id"] = str(uuid.uuid4())
        new_text = await request.app.database["texts"].insert_one(text)
        created_text = await request.app.database["texts"].find_one(
            {"_id": new_text.inserted_id}
        )

        return created_text


@router.get(
    '/',
    response_description="List all texts from a creator_id",
    response_model=List[text.Text],
    response_model_by_alias=False
)
async def list_all_texts_by_creator_id(creator_id: str, request: Request):
    texts_obj = request.app.database["texts"].find({"creator_id": creator_id}, limit=100)
    texts = await texts_obj.to_list(length=100)
    return texts


@router.get(
    '/{id}',
    response_description="Get a text by ID",
    response_model=text.Text,
    response_model_by_alias=False
)
async def find_text(id: str, request: Request):
    if (text := await request.app.database["texts"].find_one({"_id": id})) is not None:
        return text
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Text with ID {id} not found!")


@router.put(
    '/{id}',
    response_description="Update a text",
    response_model=text.Text,
    response_model_by_alias=False
)
async def update_text(id: str, request: Request, text: text.TextUpdate = Body(...)):
    text = {k: v for k, v in text.dict().items() if v is not None}
    if len(text) >= 1:
        t = await find_text(id, request)
        update_result = await request.app.database["texts"].update_one(
            {"_id": id, "creator_id": t["creator_id"]},
            {"$set": {"message": text["message"]}}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Text with ID {id} not found!")

    if (
        existing_book := await request.app.database["texts"].find_one({"_id": id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Text with ID {id} not found!")


@router.delete("/{id}", response_description="Delete a text", response_model_by_alias=False)
async def delete_text(id: str, request: Request, response: Response):
    delete_result = await request.app.database["texts"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Text with ID {id} not found")