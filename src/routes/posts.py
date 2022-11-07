from typing import Optional
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import Response
from src.models.database import get_db
from src.models import post
from src.schemas.post import PostReturn
from src.schemas.post import PostBase
from src.schemas.post import PostOut
from src import oauth2
from src.models import post
from src.models import vote
from sqlalchemy import func
# The following lines are handled by alembic
# from src.models.database import engine
# post.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/posts',
    tags=["Posts"],
    responses={404: {"description": "Not found"}}
)

@router.post('/', response_model=PostReturn, status_code=status.HTTP_201_CREATED)
def create_post(body: PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = post.Post(owner_id=current_user.id, **body.dict())
    db.add(new_post)
    db.commit()
    return new_post


@router.get('/', response_model=list[PostOut], status_code=status.HTTP_200_OK)
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = ""):
    # Version if you want to only display user specific posts: 
    # posts = db.query(post.Post).where(post.Post.owner_id == current_user.id).all()
    # limit, offset and search are query parameters they can be used by the following url `http://localhost:8000/posts?limit=5&offset=1&search=beaches`
    # use %20 for spaces
    posts = (
        db
        .query(post.Post, func.count(vote.Vote.post_id).label('votes'))
        .join(vote.Vote, vote.Vote.post_id == post.Post.id, isouter=True)
        .group_by(post.Post.id)
        .where(post.Post.title.contains(search))
        .limit(limit)
        .offset(offset)
        .all())
    return posts


@router.get('/{id}', response_model=PostOut, status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    selected_post = (
        db
        .query(post.Post, func.count(vote.Vote.post_id).label('votes'))
        .join(vote.Vote, vote.Vote.post_id == post.Post.id, isouter=True)
        .group_by(post.Post.id)
        .where(post.Post.id == id)
        .first())
        
    if not selected_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} was not found.'
        )
    return selected_post


@router.put('/{id}', response_model=PostReturn, status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, body: PostBase, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    current_post_query = db.query(post.Post).where(post.Post.id == id)
    current_post = current_post_query.first()

    if current_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'There is no post with id={id}.'
        )

    if current_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorized to perform the requested action.'
        )

    current_post_query.update(body.dict(), synchronize_session=False)
    db.commit()
    return current_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    current_post_query = db.query(post.Post).where(post.Post.id == id)
    current_post = current_post_query.first()

    if current_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id: {id} does not exist.'
        )

    if current_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform the requested action.'
        )
    
    current_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
