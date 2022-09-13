from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_exp_mins

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, cred_exception):
    try:    
        # decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # extract id
        id: str = payload.get('user_id')

        if id is None:
            raise cred_exception

        # validate whether all the data we pass into the token is actually there
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise cred_exception

    # return id
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

    token = verify_access_token(token, cred_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
