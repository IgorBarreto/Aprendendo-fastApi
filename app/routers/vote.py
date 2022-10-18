from fastapi import status, HTTPException, Response, Depends, APIRouter

from app.schemas import Vote as voteSchema
from app.models import Vote as voteModel, Post as postModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.oAuth2 import get_current_user
from app.schemas import User as userSchema

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: voteSchema,
    db: Session = Depends(get_db),
    current_user: userSchema = Depends(get_current_user),
):
    post = db.query(voteModel).filter(voteModel.post_id == postModel.id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist"
        )
    vote_query = db.query(voteModel).filter(
        voteModel.post_id == vote.post_id, voteModel.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already voted on post",
            )
        new_vote = voteModel(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Sucessfully added vote"}
    elif vote.dir > 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorret value to dir field. Acept 1 or 0",
        )
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Sucessfully deleted vote"}
