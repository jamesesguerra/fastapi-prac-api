from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix='/votes', tags=['Votes'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {vote.post_id} not found')

    found_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    if (vote.direction == 1):
        # checks if this specific user has already voted on this post
        if found_vote.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        # cant unvote if vote doesn't exist in the first place
        if not found_vote.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')

        found_vote.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)



        

