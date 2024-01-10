import datetime
import json
import uuid
from typing import Optional, List
from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId


PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    id: Optional[PyObjectId] = Field(default=uuid.uuid4(), alias="_id")
    username: str = Field(...)
    bio: str = Field(...)
    location: str = Field(...)
    texts: list = Field(...)
    created: datetime.datetime = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "06dh6409-b0a7-1k30-i84a-32537c7d1d9e",
                "username": "hochoym",
                "bio": "This is a message I'm using to test this model",
                "location": "Hartford, CT",
                "texts": [
                    {
                        "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                        "creator": "hochoym",
                        "message": "This is a message I'm using to test this model",
                        "date": datetime.datetime.now()
                    },
                ],
                "created": datetime.datetime.now()
            }
        }
    )


class UserUpdate(BaseModel):
    username: Optional[str]
    bio: Optional[str]
    location: Optional[str]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "username": "hochoym",
                "bio": "This is a message I'm using to test this model",
                "location": "Hartford, CT",
            }
        }
    )


class UserCollection(BaseModel):
    users: List[User]