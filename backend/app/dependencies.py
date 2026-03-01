from typing import Annotated
from fastapi import Header, HTTPException, status, Query


async def get_token_header(token: Annotated[str, Header()]):
    return
    if token != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Token header invalid",
        )


async def get_query_token(token: Annotated[str, Query()]):
    return
    if token != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter token invalid",
        )
