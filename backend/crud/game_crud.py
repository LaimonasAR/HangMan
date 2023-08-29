from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from models.games import Game
import schemas.game_schemas
from models.account import Account
import schemas.account_schemas


def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


def get_games(db: Session, account_id: int):
    return (
        db.query(Game)
        .filter(Game.account_id == account_id)
        .all()
    )


def create_game(
    db: Session,
    account_id,
    game: schemas.game_schemas.GameCreate,
):
    db_account = get_account(db, account_id)
    if db_account:
        db_game = Game(
            word=game.word,
            status=game.status,
            corrlett=game.corrlett,
            incorrlett=game.incorrlett,
            error_count=game.error_count,
        )
        db_account.games.append(db_game)
        db.add(db_game)
        db.commit()
        db.refresh(db_game)
        return db_game
    else:
        return NoResultFound


def get_game_score(db: Session, account_id: int):
    games = list(
        db.query(Game)
        .filter(Game.account_id == account_id)
        .all()
    )
    if games:
        totals = 0
        for game in games:
            if game.status is True :
                totals += (10 - game.error_count)
            elif game.status is False:
                totals -= game.error_count
        return totals
    else:
        return NoResultFound
