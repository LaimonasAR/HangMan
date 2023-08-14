from pydantic import BaseModel


class GameCreate(BaseModel):
    word: str
    status: bool
    corrlett: str
    incorrlett: str
    error_count: int
    # account_id: int

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                # "id": 1,
                "word": "werewolf",
                "status": True,
                "corrlett": "abcd",
                "incorrlett": "vwxyz",
                "error_count": 5,
                # "account_id": 1,
            }
        }


class GameResponse(BaseModel):
    word: str
    status: bool
    corrlett: str
    incorrlett: str
    error_count: int
    # account_id: int

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "word": "werewolf",
                "status": True,
                "corrlett": "abcd",
                "incorrlett": "vwxyz",
                "error_count": 5,
                # "account_id": 1,
            }
        }


class ScoreResponse(BaseModel):
    totals: int
