#!/usr/bin/python3
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, AfterValidator, Field, HttpUrl
from typing import Annotated, Literal
from enum import Enum

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int| str):
#     return {"item_id": item_id}


# 路径顺序 测试
# 固定路径 优先于 动态路径
@app.get('/user/me')
def read_user_me():
    return {"user_id": "the current user"}


@app.get('/user/{user_id}')
def read_user(user_id: str):
    return {'user_id': user_id}


class StudentName(str, Enum):
    alice = "alice"
    bob = "bob"
    charlie = "charlie"
    ray = 'ray'


@app.get('/students/{student_name}')
def read_student(student_name: StudentName):
    match student_name:
        case StudentName.ray:
            return {"student_name": student_name, "message": "Hello 帅帅的周睿!"}
        case _:
            return {"student_name": student_name, "message": "Fuck you!"}


@app.get('/files/{file_path:path}')
def read_file(file_path):
    return {
        'file_path': file_path,
        'msg': f'file_path is {file_path}'
    }


item_list = [{'name': 'zr', 'age': 18}, {
    "name": "example", "age": 20}, {"name": "test", "age": 22}]
# @app.get('/items/')
# def read_item(skip: int = 0, limit: int = 10):
#     return item_list[skip: skip + limit]

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


# class Item(BaseModel):
#     """商品模型"""
#     name: str = Field(..., description="商品名称", examples=["iPhone"])
#     age: int = Field(..., description="商品年限", ge=0, examples=[2])
#     description: str | None = Field(None, description="商品详细描述")
#     loc: str = Field(..., description="商品产地",
#                      examples=['China'], max_length=10)


class OtherItem(BaseModel):
    title: str
    description: str | None = None
    price: float
    tax: float | None = None


# @app.post('/items/')
# def create_item(item: Item):
#     item.name = f'{item.name}超级'
#     item_dict = item.model_dump()
#     return item_dict


# @app.put('/items/{item_id}')
# def update_item(item_id: int, item: Item,q: str| None =None):
#     result = {'item_id': item_id, **item.model_dump()}
#     if q is not None:
#         result.update({'q': q})
#     return result
# def update_item(*,
#                 item_id: Annotated[int, Path(title='The id of the item to update', ge=0, le=1000)],
#                 # query_item: Annotated[str | None, Query(max_length=20)] = None,
#                 # 单个值直接被解析为查询参数
#                 query_item: str | int | None = None,
#                 item: Annotated[Item | None, Body(embed=True)] = None,
#                 other_item: OtherItem | None = None,
#                 body_item: Annotated[int | str | None, Body()] = None,
#                 ):
#     res: dict[str, str | int | None] = {
#         'item_id': item_id,
#     }
#     if query_item is not None:
#         res.update({'query_item': query_item})
#     if item is not None:
#         res.update(item.model_dump())
#     if other_item is not None:
#         res.update(other_item.model_dump())
#     if body_item is not None:
#         res.update({'body_item': body_item})
#     return res
# def update_item(*,
#                 item_id: Annotated[int, Path(title='The id of the item to update', ge=0, le=1000)],
#                 # item: Item | None = None,
#                 item: Annotated[Item, Body(embed=True)],
#                 ):
#     return {
#         'item_id': item_id,
#         **(item.model_dump() if item else {})
    # }


@app.get('/items/')
# def read_items(q: Annotated[str|None, Query(max_length=10, min_length=3)] = '草泥马'):
#     results = {
#         'items': item_list
#     }
#     if q:
#         results.update({'q': q})
#     return results
# def read_items(q:Annotated[str,Query(min_length=3)]):
#     res = {
#         'name':'你要鸡把干啥'
#     }
#     if q is not None:
#         res.update({'q': f'草拟的:{q}'})
#     return res
# def read_items(q: Annotated[list[str],Query(title="test query title",description ='test query description',max_length=10,alias='name',deprecated=True)] ):
#     res={
#         'list':q
#     }
#     return res
# 在文档中 隐藏查询参数
# def read_items(q:Annotated[str,Query(include_in_schema=False)]):
#     return {
#         "q":q
#     }
def check_valid_query(value: str):
    if value != 'zr':
        raise ValueError('查询参数不合法')
    return value


# def read_items(q:Annotated[str|None,Query(max_length=5,),AfterValidator(check_valid_query)] = None):
#     return {
#         "q":q
#     }


@app.get('/items/{item_id}')
def read_items(item_id: Annotated[int, Path(title='title of test path', gt=0, le=3)], q: Annotated[str | None, Query(max_length=10)] = None):
    results: dict[str, int | str] = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


class ProductNest(BaseModel):
    name: str
    price: float
    url: HttpUrl


class FilterPars(BaseModel):
    model_config = {'extra': 'forbid'}
    limit: int = Field(10, gt=0, le=10)
    offset: int = Field(0, ge=0)
    order_by: Literal['asc', 'desc'] = 'asc'
    tags: list[str] | None = None
    set_tags: set[str] | None = None
    # product_nest: ProductNest
    products: list[ProductNest] | None = None


class DeepNestProduct(BaseModel):
    name: str
    details: FilterPars | None = None


@app.get('/products/')
def read_products(filter_query: Annotated[FilterPars, Query()]):
    return filter_query


@app.put('/products/{product_id}')
def update_product(
    product_id: int,
    product: Annotated[DeepNestProduct, Body(embed=True)]


):
    return {
        'product_id': product_id,
        **product.model_dump()
    }


#  声明请求示例数据
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class AnimalItem(BaseModel):
    name: str = Field(..., examples=["dog", "cat"])
    age: int = Field(..., ge=0, examples=[3, 5])
    description: str | None = Field(
        None, examples=["A friendly dog", "A cute cat"])
    remark: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "dog",
                    "age": 3,
                    "description": "A friendly dog",
                    "remark": "no remarks"
                },
                {
                    "name": "cat",
                    "age": 5,
                    "description": "A cute cat",
                    "remark": "no remarks"
                }
            ]
        }
    }


@app.post('/animals/')
def create_animal(animal: Annotated[AnimalItem, Body(openapi_examples={
    'normal_example': {
        'summary': '正常例子',
        'description': '这是一个正常的例子',
        'value': {
            "name": "dog",
            "age": 3,
            "description": "A friendly dog",
            "remark": "no remarks"
        },
    },
    'invalid_example': {
        'summary': '无效示例',
        'description': '缺少必填字段的无效示例',
        'value': {
            "name": "cat",
            "age": -1,
            "description": "A friendly dog",
        }
    }
})]):
    return animal.model_dump()


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results


# 额外数据类型

# if __name__ == "__main__":
#     main()
