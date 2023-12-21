from os import environ as env
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from models import Users
from database import get_db
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

JSON_SECRET = env.get("JSON_SECRET")
JSON_ALG = env.get("JSON_ALG")


class UserCreate(BaseModel):
    name: str
    alt_name: str
    email: str
    password: str
    role: str

    class Config:
        json_schema_extra = {
            "example": {
              "name": "Jonathan Fernandes",
              "alt_name": "",
              "email": "jonathan_fernandes@bjsmicschool.com",
              "password": "123456",
              "role": "admin"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": email, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, JSON_SECRET, algorithm=JSON_ALG)


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = Users(**user.model_dump())
    new_user.password = bcrypt_context.hash(user.password)

    db.add(new_user)
    db.commit()


@router.post("/token", response_model=Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password

    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    token = create_access_token(user.email, user.id, timedelta(minutes=90))
    return {"access_token": token, "token_type": "bearer"}
