from fastapi import Depends, status, APIRouter
from fastapi import HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prifix='/vote',
    tags=['Votes'],
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user_id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user : {current_user_id} has already voted on the post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user_id)
        db.add(new_vote)
        db.commit()
        return {'message' : 'successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message' : 'successfully deleted'}