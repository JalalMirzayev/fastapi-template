from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.schemas.user import UserCreate
from src.schemas.user import UserReturn
from src.utils import hash
from src.models import user

# The following lines are handled by alembic
# from src.models.database import engine
# user.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={404: {"description": "Not found"}})


@router.post('/', response_model=UserReturn, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, db: Session=Depends(get_db)):
    body.password = hash(body.password)
    new_user = user.User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', response_model=list[UserReturn], status_code=status.HTTP_200_OK)
def get_users(db: Session=Depends(get_db)):
    users = db.query(user.User).all()
    return users


@router.get('/{id}', response_model=UserReturn, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session=Depends(get_db)):
    user_result = db.query(user.User).where(user.User.id == id).first()
    if not user_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id: {id} not found.'
        )
    return user_result
