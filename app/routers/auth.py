from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas
from ..database import get_db


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login', response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()

    # if email isn't in the DB
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials.')

    # validate password
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials.')

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

