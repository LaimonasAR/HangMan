from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class AccountCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                # "id": 1,
                "name": "Antanas",
                "surname": "Fontanas",
                "email": "antanas123@gmail.com",
                "password": "1234",
            }
        }

class AccountResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Antanas",
                "surname": "Fontanas",
                "email": "antanas123@gmail.com",
                "password": "1234",
            }
        }

class AccountUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr]

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Antanas",
                "surname": "Fontanas",
                "email": "antanas123@gmail.com",
                "password": "1234",
            }
        }