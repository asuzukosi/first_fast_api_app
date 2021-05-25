from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from .database import get_db
from .models import User
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        user_email = data["email"]

        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token contains invalid credentials")
        return user
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
