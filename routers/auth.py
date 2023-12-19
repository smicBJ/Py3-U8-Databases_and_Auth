from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import Users
from database import get_db

router = APIRouter()


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


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = Users(**user.model_dump())

    db.add(new_user)
    db.commit()
