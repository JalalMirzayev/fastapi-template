from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.models import vote
from src.models import post
from src.oauth2 import get_current_user
from src.schemas.vote import VoteReturn
from src.schemas.vote import Vote
from src.models.database import engine
vote.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix='/vote',
    tags=['Vote'],
     responses={404: {"description": "Not found"}})


@router.post('/', response_model=dict, status_code=status.HTTP_201_CREATED)
def set_vote(body: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    current_post = db.query(post.Post).where(post.Post.id == body.post_id).first()
    
    if current_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {body.post_id} does not exist.'
        )

    vote_query = db.query(vote.Vote).where(vote.Vote.post_id == body.post_id, vote.Vote.user_id == current_user.id)
    current_vote = vote_query.first()

    if (body.direction == 1):
        # If the vote has already been done
        if current_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User with id: {current_user.id} has already voted on post {body.post_id}.')
        new_vote = vote.Vote(post_id=body.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        # If you want to delete a non existing vote
        if not current_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Vote does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message': 'successfully deleted vote'}


@router.get('/', response_model=list[VoteReturn])
def get_votes(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    current_votes = db.query(vote.Vote).all()
    return current_votes
