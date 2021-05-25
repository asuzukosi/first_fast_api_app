from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from .. import database
from .. import hashing
# schemas, database, hashing
from fastapi import HTTPException, status


router = APIRouter(tags=["User"], prefix="/user")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserShow)
def create_user(user: schemas.User, db: Session = Depends(database.get_db)):
    hasher = hashing.Hash()
    hashed_password = hasher.bcrypt(user.password)
    new_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("{pk}/", response_model=schemas.UserShow, tags=["User"])
def get_speicfic_user(pk: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == pk).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {pk} does not exist")

    return user


@router.get("/", response_model= List[schemas.UserShow], tags=["User"])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users
