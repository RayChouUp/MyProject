from fastapi import APIRouter
from sqlmodel import Session,Table, SQLModel, Field, create_engine, select
import jwt 

router = APIRouter()

class UserBase(SQLModel):
    username: str

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str

@app.post('/users/', tags=["users"], summary="Create a user", response_description="The created user")
def create_user(user: UserBase,session: Session):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get('/users/', tags=["users"], summary="Get all users", response_description="List of users")
async def get_users():
    return [{"username": "user1"}, {"username": "user2"}]
