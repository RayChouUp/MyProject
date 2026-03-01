from fastapi import APIRouter, Depends

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@router.get("/")
async def read_admin_dashboard():
    return {"message": "Admin dashboard"}


@router.get("/settings")
async def read_admin_settings():
    return {"message": "Admin settings"}
