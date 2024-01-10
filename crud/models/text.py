import datetime
import uuid
from typing import Optional, List
from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId


PyObjectId = Annotated[str, BeforeValidator(str)]


class Text(BaseModel):
    id: PyObjectId = Field(default=uuid.uuid4(), alias="_id")
    creator_id: PyObjectId = Field(...)
    message: str = Field(...)
    date: datetime.datetime = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "creator_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "message": "This is a message I'm using to test this model",
                "date": datetime.datetime.now()
            }
        }
    )


class TextUpdate(BaseModel):
    message: Optional[str]

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "message": "This is a message I'm using to test this model",
            }
        }
    )


class TextCollection(BaseModel):
    texts: List[Text]
