from fastapi import APIRouter, Depends, HTTPException

from schemas.game_schemas import (
    GameCreate,
    GameResponse,
    ScoreResponse
)
import crud.game_crud
import crud.account_crud
from database.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{account_id}", response_model=list[GameResponse])
def read_games(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.account_crud.get_account(db, account_id=account_id)
    if db_account:
        games = crud.game_crud.get_games(db, account_id)
        return games
    else:
        raise HTTPException(status_code=404, detail=f"account {account_id} not found")


@router.post("/{account_id}", response_model=GameResponse)
def create_game(
    account_id: int,
    game: GameCreate,
    db: Session = Depends(get_db),
):
    db_account = crud.account_crud.get_account(db, account_id)
    if db_account:
        return crud.game_crud.create_game(db=db, account_id=account_id, game=game)
    else:
        raise HTTPException(status_code=404, detail=f"account {account_id} not found")


@router.get("/{account_id}/totals", response_model=ScoreResponse)
def get_totals(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.account_crud.get_account(db, account_id=account_id)
    if db_account:
        totals = crud.game_crud.get_game_score(db, account_id)
        return {"totals": totals}
    else:
        raise HTTPException(status_code=404, detail=f"account {account_id} not found")
