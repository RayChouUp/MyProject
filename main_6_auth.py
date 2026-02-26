from fastapi import FastAPI, Depends, status, HTTPException, Header, Query
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pathlib import Path as SysPath
from pydantic import BaseModel, EmailStr
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError

INDEXHTML = SysPath(__file__).resolve().parent / "view" / "index.html"
SECRET_KEY = "c529450dbc9f5b614b0bb90c4f7e6a02e0a55a7df88881c61241fb5b704ccbb4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()


@app.get('/')
def read_root():
    return FileResponse(INDEXHTML)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


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
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"
    },
}

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDb(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15, hours=1)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_user_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    crentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='verify token failed',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise crentials_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise crentials_exception
    user = get_user(fake_user_db, username=token_data.username)
    if user is None:
        raise crentials_exception
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
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_dict = fake_user_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(
#             status_code=400, detail="Incorrect username or password")
#     user = UserInDb(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(
#             status_code=400, detail="Incorrect username or password")
#     return {"access_token": user.username + "token", "token_type": "bearer"}
async def login_with_realtoken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(
        fake_user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get('/users/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_enabled_user)]):
    return current_user


if __name__ == "__main__":
    print("Hello, World!")
