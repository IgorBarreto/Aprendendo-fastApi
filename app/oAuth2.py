from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas import TokenData as TokenDataSchema, User as UserSchema
from app.database import get_db
from app.models import User as UserModel


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "c82d1b07d7f2b4f5bb18e4ede23b1347f863e748"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_DAYS = 1


def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=ACESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_acess_token(token: str, credetials_exception):
    try:
        payload_data = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload_data.get("user_id")
        if not id:
            raise credetials_exception
        token_data = TokenDataSchema(id=id)
    except JWTError:
        raise credetials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db),
) -> UserSchema:
    credetials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_acess_token(token, credetials_exception)
    user = db.query(UserModel).filter(UserModel.id == token.id).first()
    return user
