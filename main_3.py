from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path as SysPath
from typing import Annotated
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
app = FastAPI()
INDEX_FILE = SysPath(__file__).resolve().parent / "view" / "index.html"


class EnumModel(Enum):
    tag_one = '标签1'
    tag_two = '标签2'


@app.get('/')
def read_root():
    return FileResponse(INDEX_FILE)


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: StarletteHTTPException):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    # message = "Validation error: " + \
    #     "; ".join([f"{err['loc']}: {err['msg']}" for err in exc.errors()])
    # return PlainTextResponse(message, status_code=400)
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

itemDict = {
    'zr': {"name": "Item 1", "description": "This is item 1"},
}


@app.get("/items/{item_id}", tags=[EnumModel.tag_one])
async def read_item(item_id: Annotated[str, Path(..., title="The ID of the item to get")]):
    if item_id in itemDict:
        return itemDict[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found", headers={
                            "X-Error": "There goes my error"})


@app.get("/unicorns/{item_id}")
async def read_unicorn(item_id: str):
    if item_id not in itemDict:
        raise UnicornException(name=item_id)
    return itemDict[item_id]


@app.get("/cover_default_exceptions/{item_id}", deprecated=True)
async def read_item_with_covered_exceptions(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
        raise RequestValidationError(errors=[{
            "loc": ["path", "item_id"],
            "msg": "Item not found",
            "type": "value_error.item_not_found"
        }])
    return {"item_id": item_id}


class Item(BaseModel):
    model_config = {
        "extra": 'forbid'
    }
    name: str
    description: str | None = None


@app.post('/items/', status_code=status.HTTP_201_CREATED, tags=[EnumModel.tag_one], summary="Create an item", response_description="Return the created item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item.model_dump()


class Student(BaseModel):
    model_config = {'extra': 'forbid'}
    student_id: str
    student_name: str = 'Unknown'
    student_score: float | None = None
    created_at: datetime = datetime.now()
    tags: list[str] = []


studentsList = {
    's1': Student(student_id='student1', student_name='Alice', student_score=95.5, tags=['excellent', 'diligent']),
    's2': Student(student_id='student2', student_name='Bob'),
    's3': {'student_id': 'student3'}
}


@app.put('/students/{student_id}', tags=['student'])
async def update_student(student_id: str, student: Student):
    if student_id in studentsList:
        stored_student_data = studentsList[student_id]
        if isinstance(stored_student_data, Student):
            stored_student_model = stored_student_data
        elif isinstance(stored_student_data, dict):
            stored_student_model = Student(**stored_student_data)
        else:
            raise HTTPException(
                status_code=500, detail="Invalid stored student data")
        update_student_data = student.model_dump(exclude_unset=True)
        updated_student = stored_student_model.model_copy(
            update=update_student_data)
        studentsList[student_id] = updated_student
        return studentsList
    else:
        raise HTTPException(status_code=404, detail="Student not found")
if __name__ == "__main__":
    print("Hello, World!")
