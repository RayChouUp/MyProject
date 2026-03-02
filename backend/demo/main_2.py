from fastapi import FastAPI, Path, Query, Body, Cookie, Response, Header, status, Form, File, UploadFile, HTTPException
from typing import Annotated, Any, Union
from pathlib import Path as SysPath
from pydantic import BaseModel, EmailStr
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse, HTMLResponse


app = FastAPI()
INDEX_FILE = SysPath(__file__).resolve().parent / "view" / "index.html"


# @app.get('/items/')
# def read_items(asc_id: Annotated[str | None, Cookie()] = None,):
#     return {'asc_id': asc_id}


# @app.get('/set-cookie/')
# def set_cookie(response: Response):
#     response.set_cookie(key="asc_id", value="test123")
#     return {"message": "Cookie 已设置"}

@app.get('/')
def read_root():
    return FileResponse(INDEX_FILE)


@app.get("/user")
def read_user(user_agent: Annotated[str | None, Header()] = None, custom_agent: Annotated[str | None, Header(convert_underscores=False)] = None, custom_token: Annotated[list[str] | None, Header(convert_underscores=False)] = None):
    return {"user_agent": user_agent, "custom_agent": custom_agent, "custom_token": custom_token}


class Cookies(BaseModel):
    model_config = {'extra': 'forbid'}
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


class DogCookies(BaseModel):
    dog_id: str
    dog_tracker: str | None = None


@app.get('/dogs')
def read_dogs(cookies: Annotated[DogCookies | None, Cookie()] = None):
    return {"cookies": cookies}


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies


class Cats(BaseModel):
    model_config = {'extra': 'forbid'}
    cat_id: str
    cat_tracker: str | None = None


@app.get('/cats')
def read_cats(cats_header: Annotated[Cats, Header()]):
    return {"cats_header": cats_header}


class Cars(BaseModel):
    model_config = {'extra': 'forbid'}
    car_id: int | str
    car_name: str | None = None
    car_price: float


@app.post('/cars', response_model=Cars)
def create_car(cars: Annotated[Cars, Body()]) -> Any:
    return cars


@app.get('/cars/')
def read_car() -> list[dict]:
    return [
        {"car_id": 1, "car_name": "Toyota", "car_price": 30000.0},
        {"car_id": 2, "car_name": "Honda", "car_price": 28000.0},
    ]


# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr


# class UserOut(BaseModel):
#     username: str
#     email: EmailStr


# @app.post('/users/', response_model=UserOut)
# # def create_user(user: Annotated[UserIn, Body()]) -> Any:
# #     return user
# def create_user(user: UserIn) -> Any:
#     return user
    # return UserOut(username=user.username+'123', email=user.email)


class BaseCustomer(BaseModel):
    name: str
    age: int


class vipCustomer(BaseCustomer):
    # model_config = {'extra': 'forbid'}
    vip_level: str
    money_spent: float


@app.post('/customers/')
def create_customer(customer: vipCustomer) -> BaseCustomer:
    return customer


@app.get('/teleport/')
def get_teleport(teleport_flag: Annotated[bool | None, Query()] = False) -> Response:
    if teleport_flag:
        return RedirectResponse(url="https://www.fastapi.tiangolo.com/")
    else:
        return JSONResponse(content={"message": "No teleportation occurred."})


@app.get('/redirecttest/', response_model=None)
# invalid redirect example
def redirect_test(redirect_flag: Annotated[bool | None, Query()] = False) -> Response | dict:
    return RedirectResponse(url="/teleport/?teleport_flag=true")


class Beauties(BaseModel):
    model_config = {'extra': 'forbid'}
    beauty_id: int
    beauty_name: str = 'Unknown'
    beauty_score: float | None = None
    tags: list[str] = []


beauties = {
    'beauty1': Beauties(beauty_id=1, beauty_name='Alice', beauty_score=9.5, tags=['elegant', 'charming']),
    'beauty2': Beauties(beauty_id=2, beauty_name='Bella'),
    'beauty3': {'beauty_id': 3}
}


@app.get('/beauties/', response_model=Beauties, response_model_include={'beauty_id', 'beauty_name'})
def get_beauty(beauty_id: str):
    return beauties[beauty_id]


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    pass


class UserInDb(BaseUser):
    hashed_password: str


def fake_hash_password(password: str) -> str:
    return "hashed_" + password


def fake_save_user(user_in: UserIn) -> UserInDb:
    hashed_password = fake_hash_password(user_in.password)
    user_in_db = UserInDb(
        **user_in.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )
    print("User saved! ..not really", user_in_db)
    return user_in_db


@app.post('/users/', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_random1(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


class ManModel(BaseModel):
    name: str
    age: int
    sex: str = 'male'


class WomanModel(BaseModel):
    name: str
    age: int
    sex: str = 'female'


@app.post('/people/', response_model=ManModel | WomanModel, status_code=201)
def create_person(person: Annotated[ManModel | WomanModel, Body()]) -> Any:
    return person


@app.post('/login/')
def login(username: Annotated[str, Form()], password: Annotated[str, Form()]) -> dict:
    if username == "admin" and password == "secret":
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid credentials"}


class FormDataModel(BaseModel):
    name: str
    age: int


@app.post('/create-user/', status_code=201)
def create_user(data: Annotated[FormDataModel, Form()]) -> dict:
    return data.model_dump()


@app.post('/files/')
async def create_file(file: Annotated[bytes | None, File(description='A file read as bytes')]):
    if file is None:
        return {"message": "No file uploaded"}
    else:
        return {"file_size": len(file)}


@app.post('/uploadfile/')
async def create_upload_file(file: Annotated[UploadFile | None, File(description='A file read as UploadFile')]):
    if file is None:
        return {"message": "No file uploaded"}
    else:
        return {"filename": file.filename, "content_type": file.content_type}


@app.post('/files_multiple/')
async def create_files(files: Annotated[list[bytes] | None, File(description='Multiple files read as bytes')]):
    if files is None:
        return {"message": "No files uploaded"}
    else:
        return {"file_sizes": [len(file) for file in files]}


@app.post('/uploadfiles_multiple/')
async def create_upload_files(files: Annotated[list[UploadFile] | None, File(description='Multiple files read as UploadFile')]):
    if files is None:
        return {"message": "No files uploaded"}
    else:
        return {"filenames": [file.filename for file in files], "content_types": [file.content_type for file in files]}


# @app.get('/testfile/')
# async def test_file():
#     content = """
#     <html>
#         <head>
#             <title>Test File</title>
#         </head>
#         <body>
#             <h1>This is a test file</h1>
#             <p>Hello, this is a test file for FastAPI.</p>

#     <form action="/files_multiple/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles_multiple/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=content)

@app.post('/fileandform/')
async def create_file_and_form(
    file: Annotated[bytes | None, File(description='A file read as bytes')],
    upload_file: Annotated[UploadFile | None, File(description='A file read as UploadFile')],
    token: Annotated[str, Form()]
):
    file_size = len(file) if file is not None else 0
    upload_file_info = None

    if upload_file is not None:
        upload_content = await upload_file.read()
        upload_file_info = {
            "filename": upload_file.filename,
            "content_type": upload_file.content_type,
            "file_size": len(upload_content)
        }

    return {
        "file_size": file_size,
        "upload_file": upload_file_info,
        "token": token
    }


if __name__ == "__main__":
    print("Hello, World!")
