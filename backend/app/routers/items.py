from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from ..dependencies import get_token_header, get_query_token
from typing import Annotated
router = APIRouter(
    prefix='/items',
    tags=["items"],
    dependencies=[Depends(get_token_header), Depends(get_query_token)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = [{"item_name": "Foo", "item_id": 0}, {
    "item_name": "Bar", "item_id": 1}, {"item_name": "Baz", "item_id": 2}]


@router.get('/{item_id}')
def get_item(item_id: Annotated[int, Path()]):
    for item in fake_items_db:
        if item["item_id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.put('/{item_id}', tags=['another_tag'], responses={404: {"description": "Item not found"}, 200: {"description": "Successful update"}})
async def update_item(
    item_id: Annotated[int, Path()],
    item: Annotated[dict, Body()]
):
    for existing_item in fake_items_db:
        if existing_item["item_id"] == item_id:
            existing_item.update(item)
            return existing_item
    raise HTTPException(status_code=404, detail="Item not found")
