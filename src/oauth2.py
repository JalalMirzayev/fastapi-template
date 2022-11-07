from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.models import user 
from jose import JWTError, jwt
from src.schemas.token import TokenData
from src.config import settings

# tokenUrl from routes/auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')

# Source: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=#hash-and-verify-the-passwords
# Open git-bash and type `openssl rand -hex 32` to obtain`
SECRET_KEY = settings.secret_key # config.get('SECRET_KEY', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
ALGORITHM = settings.algorithm # config.get('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes # config.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Argument in payload.get must be the same as in src.routes.auth
        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'})
    
    token = verify_access_token(token, credential_exception)
    current_user = db.query(user.User).where(user.User.id == token.id).first()

    return current_user