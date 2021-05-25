from .. import models
from .. import schemas
from .. import database
from .. import hashing
from .. import oauth2
# schemas, database, hashing

from sqlalchemy.orm import Session
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
import datetime

router = APIRouter(tags=["Authentication"], prefix="/authentication")


@router.post("/login/")
def login(user: schemas.Login, db: Session = Depends(database.get_db)):

    user_check = db.query(models.User).filter(models.User.email==user.email).first()
    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user with those details found")

    hasher = hashing.Hash()

    if not hasher.verify(user_check.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    payload = {
        "email": user_check.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    access_token = jwt.encode(payload, "secret", algorithm="HS256")

    return {
        "token": access_token,
        "token_type": "bearer"
    }


@router.get("/me/", response_model=schemas.UserShow)
def show_user(user: schemas.UserShow = Depends(oauth2.get_current_user)):
    return user
