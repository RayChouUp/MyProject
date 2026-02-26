from fastapi import FastAPI, HTTPException, Path, Query, status, Depends, Cookie, Response, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path as SysPath
from typing import Annotated, Any
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
INDEX_FILE = SysPath(__file__).resolve().parent / "view" / "index.html"


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "zr_niubi":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "zr_niubi_key":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid")
# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
app = FastAPI()


@app.get('/')
def read_root():
    return FileResponse(INDEX_FILE)


async def common_parameters(q: Annotated[str | None, Query()] = None, skip: int = 0, limit: int = 100):
    return {
        "q": q,
        "skip": skip,
        "limit": limit
    }

CommonDep = Annotated[dict, Depends(common_parameters)]


class CommonQueryParams:
    def __init__(self, q: Annotated[str | None, Query()], skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
# async def read_items(commons: CommonDep):
#     return commons
# async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response


@app.get("/users/")
async def read_users(commons: CommonDep):
    return commons


def extractor_query(q: Annotated[str | None, Query()] = None):
    return q


def extractor_query_or_cookie(
    q: Annotated[str, Depends(extractor_query, use_cache=False)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/rays/", tags=["rays"])
async def read_rays(query_or_default: Annotated[str, Depends(extractor_query_or_cookie)]):
    return {"q": query_or_default}


@app.get("/set-last-query/", tags=["rays"])
async def set_last_query(
    response: Response,
    last_query: Annotated[str, Query(min_length=1)],
):
    response.set_cookie(key="last_query", value=last_query)
    return {"message": "last_query cookie set", "last_query": last_query}


@app.get("/rays/headers/", tags=["rays"], dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_rays_headers():
    return {"message": "Headers are valid"}


custom_data = {
    'data1': {'name': 'zr', 'value': 123},
    'data2': {'name': 'ray', 'value': 456},
}


class OwnerError(Exception):
    pass


class InternalError(Exception):
    pass


def get_data():
    try:
        yield 'zr'
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/custom-data/{data_id}')
async def read_custom_data(data_id: str, user_name: Annotated[str, Depends(get_data)]):
    if data_id == 's':
        raise InternalError(
            f"The {data_id} is too dangerous to be owned by {user_name}"
        )

if __name__ == "__main__":
    print("Hello, World!")
