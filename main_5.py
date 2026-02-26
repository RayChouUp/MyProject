from fastapi import FastAPI, Depends, status, HTTPException, Header, Query
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pathlib import Path as SysPath
from pydantic import BaseModel, EmailStr
from pwdlib import PasswordHash
app = FastAPI()

INDEXHTML = SysPath(__file__).resolve().parent / "view" / "index.html"


@app.get('/')
def read_root():
    return FileResponse(INDEXHTML)


class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = False


class UserInDb(User):
    hashed_password: str


fake_user_db = {
    "ray": {
        "username": "ray",
        "email": "",
        "full_name": "周睿",
        "disabled": False,
        "hashed_password": "fakehashedpassword"
    },
    'hzf': {
        "username": "hzf",
        "email": "",
        "full_name": "黄展凤",
        "disabled": True,
        "hashed_password": "fakehashedpassword2"
    }
}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDb(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_user_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_enabled_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    print("current_user:", current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.post('/token/', tags=["auth"], summary="Login to get an access token", response_description="Return the access token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_user_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    user = UserInDb(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username + "token", "token_type": "bearer"}


@app.get('/users/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_enabled_user)]):
    return current_user


if __name__ == "__main__":
    print("Hello, World!")
