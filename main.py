from fastapi import FastAPI, Depends, status, HTTPException, Header, Query, Request
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from typing import Annotated, TypeAlias
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pathlib import Path as SysPath
from pydantic import BaseModel, EmailStr
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
import time
from jwt.exceptions import InvalidTokenError
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, Field, create_engine, select
INDEXHTML = SysPath(__file__).resolve().parent / "../view" / "index.html"
SECRET_KEY = "c529450dbc9f5b614b0bb90c4f7e6a02e0a55a7df88881c61241fb5b704ccbb4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://.tiangolo.com",
                   "https://.tiangolo.com",
                   "https://",
                   "https://:8080",],
    allow_methods=["*"],
)


@app.get('/')
def read_root():
    return FileResponse(INDEXHTML)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers['X-process-time'] = str(process_time)
    return response


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post('/heros/', response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get('/heros/', response_model=list[HeroPublic])
def read_heros(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    heros = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heros


@app.get('/heros/{hero_id}', response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch('/heros/{hero_id}', response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    db_hero.sqlmodel_update(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.delete('/heros/{hero_id}',)
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="No hero found")
    session.delete(hero)
    session.commit()
    return {
        'result': 'success'
    }


if __name__ == "__main__":
    print("Hello, World!")
