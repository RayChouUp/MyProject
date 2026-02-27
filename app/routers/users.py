from fastapi import APIRouter

router = APIRouter()


@router.get('/users/', tags=["users"], summary="Get all users", response_description="List of users")
async def get_users():
    return [{"username": "user1"}, {"username": "user2"}]
