from fastapi import FastAPI, Depends, status, HTTPException, Header, Query, Request
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, RedirectResponse
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
FRONTEND_DIST = (SysPath(__file__).resolve().parent / "../../frontend/dist").resolve()
FRONTEND_INDEX = FRONTEND_DIST / "index.html"
FRONTEND_DEV_URL = "http://localhost:5173"
# STATIC_DIR = SysPath(__file__).resolve().parent / "static"

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+)(:\d+)?",
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

# app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get('/')
def read_root(request: Request):
    if FRONTEND_INDEX.exists():
        return FileResponse(str(FRONTEND_INDEX))
    host = request.url.hostname or "localhost"
    return RedirectResponse(url=f"http://{host}:5173")


@app.get('/{full_path:path}')
def serve_spa(full_path: str, request: Request):
    file_path = (FRONTEND_DIST / full_path).resolve()
    if FRONTEND_DIST in file_path.parents and file_path.exists() and file_path.is_file():
        return FileResponse(str(file_path))
    if FRONTEND_INDEX.exists():
        return FileResponse(str(FRONTEND_INDEX))
    host = request.url.hostname or "localhost"
    return RedirectResponse(url=f"http://{host}:5173/{full_path}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Hello, World!")
