from fastapi import FastAPI, Depends, status, HTTPException, Header, Query, Request
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from typing import Annotated
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
from .dependencies import get_token_header, get_query_token
from .routers import users, items, notification
from .internal import admin
from fastapi.staticfiles import StaticFiles
import uvicorn
INDEXHTML = SysPath(__file__).resolve().parent / "../view" / "index.html"
STATIC_DIR = SysPath(__file__).resolve().parent / "static"

description = """
个人项目

"""

app = FastAPI(
    description=description,
    version="0.1.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "RayChou 周睿",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(notification.router)
app.include_router(admin.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://.tiangolo.com",
                   "https://.tiangolo.com",
                   "https://",
                   "https://:8080",],
    allow_methods=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get('/')
def read_root():
    return FileResponse(INDEXHTML)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Hello, World!")
