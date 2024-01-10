import uuid
import routes.texts
import fastapi.exceptions
import pymongo.errors

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId

from crud.models import user

router = APIRouter()


@router.post(
    '/',
    response_description="Create a user",
    status_code=status.HTTP_201_CREATED,
    response_model=user.User,
    response_model_by_alias=False
)
async def create_user(request: Request, user: user.User = Body(...)):
    try:
        user = jsonable_encoder(user)
        if u := await request.app.database["users"].find_one(user['username']):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists!")
        else:
            new_user = await request.app.database["users"].insert_one(user)
            created_user = await request.app.database["users"].find_one(
                {"_id": new_user.inserted_id}
            )

            return created_user

    except fastapi.exceptions.ResponseValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        print(e.msg)
        pass
    except pymongo.errors.DuplicateKeyError as d:
        user = jsonable_encoder(user)
        if u := await request.app.database["users"].find_one(user['username']):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists!")
        else:
            user["_id"] = str(uuid.uuid4())
            new_user = await request.app.database["users"].insert_one(user)
            created_user = await request.app.database["users"].find_one(
                {"_id": new_user.inserted_id}
            )

            return created_user


@router.get(
    '/{id}',
    response_description="Get a user by ID",
    response_model=user.User,
    response_model_by_alias=False
)
async def find_user(id: str, request: Request):
    if (user := await request.app.database["users"].find_one({"_id": id})) is not None:
        user['texts'] = await routes.texts.list_all_texts_by_creator_id(user["_id"], request)
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found!")


@router.get('/', response_description="Get a user by username", response_model=user.User, response_model_by_alias=False)
async def find_user_by_username(username: str, request: Request):
    if (user := await request.app.database["users"].find_one({"username": username})) is not None:
        user['texts'] = await routes.texts.list_all_texts_by_creator_id(user["_id"], request)
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found!")


@router.put('/{id}', response_description="Update a user", response_model=user.User, response_model_by_alias=False)
async def update_user(id: str, request: Request, user: user.UserUpdate = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = await request.app.database["users"].update_one(
            {"_id": id}, {"$set": user}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found!")

    if (
        existing_user := await request.app.database["users"].find_one({"_id": id})
    ) is not None:
        return existing_user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found!")


@router.delete("/{id}", response_description="Delete a user", response_model_by_alias=False)
async def delete_user(id: str, request: Request, response: Response):
    delete_result = await request.app.database["users"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")