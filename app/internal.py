from fastapi import APIRouter

router = APIRouter(
    # prefix='/admin',
    # tags=["admin"],
    # responses={404: {"description": "Not found"}},
)


@router.get('/')
def read_admin():
    return {"message": "Admin endpoint"}
