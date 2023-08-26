from fastapi import APIRouter, Depends, status, HTTPException

from schemas.account_schemas import AccountCreate, AccountResponse, AccountUpdate
import crud.account_crud
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter()


@router.post("/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = crud.account_crud.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.account_crud.create_account(db=db, account=account)


@router.get("/", response_model=list[AccountResponse])
def read_accounts(db: Session = Depends(get_db)):
    accounts = crud.account_crud.get_accounts(db)
    return accounts

@router.get("/{email}", response_model=AccountResponse)
def read_account(email: str, db: Session = Depends(get_db)):
    db_account = crud.account_crud.get_account_by_email(db, email=email)
    if db_account is None:
        raise HTTPException(status_code=404, detail=f"account {email} not found")
    return db_account

@router.get("/account/{account_id}", response_model=AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.account_crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail=f"account {account_id} not found")
    return db_account


@router.delete("/{account_id}", response_model=AccountResponse)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    try:
        db_account = crud.account_crud.delete_account(db, account_id=account_id)
        return db_account
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"account {account_id} not found")


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account: AccountUpdate, account_id: int, db: Session = Depends(get_db)
):
    try:
        db_account = crud.account_crud.update_account(
            db, account_id=account_id, account=account
        )  # asdadadadsaddad
        return db_account
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"account {account_id} not found")
