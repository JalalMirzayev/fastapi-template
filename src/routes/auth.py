from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.models import user
from src.schemas.user import UserLogin
from src.utils import hash, verify
from src import oauth2
from src.schemas.token import Token

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    responses={404: {'description': 'Not found'}}
)

@router.post('/', response_model=Token, status_code=status.HTTP_200_OK)
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    hashed_password = hash(body.password)
    current_user = db.query(user.User).where(user.User.email == body.username).first()

    if not current_user:
        # Do not give away information if password or email is incorrect.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Invalid Credentials.')

    if not verify(body.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Invalid Credentials.'
        )

    access_token = oauth2.create_access_token(data={'user_id': current_user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
