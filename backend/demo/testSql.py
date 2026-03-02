from fastapi import FastAPI, Request
from sqlmodel import SQLModel,Session, Field, create_engine, select

class HeroBase(SQLModel):
        name:str 
        secret_name:str
        age:int | None = None

class Hero(HeroBase, table=True):
    id: int| None = Field(default=None, primary_key=True)

db_url = 'sqlite:///database.db'
engine = create_engine(db_url, echo=True)

def create_db_and_tables():
     SQLModel.metadata.create_all(engine)

app = FastAPI()


def create_heroes():
     hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
     hero_2 = Hero(name="Spider-Boy", secret_name="Miles Morales", age=16)
     hero_3 = Hero(name="Rusty-Man", secret_name="Rusty Wilson", age=30)
     with Session(engine) as session:
          session.add(hero_1)
          session.add(hero_2)
          session.add(hero_3)
          session.commit()

def init():
     create_db_and_tables()
     create_heroes()    


@app.on_event("startup")
def on_startup():
     init()

if __name__ == "__main__":
    pass
