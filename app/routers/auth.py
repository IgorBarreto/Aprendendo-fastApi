from fastapi import APIRouter, Depends, status, HTTPException, responses
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.database import get_db
from app.schemas import Token as TokenSchema, TokenData as TokenDataSchema, UserLogin
from app.models import User as userModel
from app.utils import verify_password
from app.oAuth2 import create_acess_token

router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)


@router.post("/", response_model=TokenSchema)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(userModel).filter(userModel.email == user_credentials.username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect Email e/or passowrd",
        )
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect Email e/or passowrd",
        )
    acess_token = create_acess_token(
        data={"user_id": user.id},
    )
    return {"acess_token": acess_token, "token_type": "bearer"}
