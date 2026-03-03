from fastapi import FastAPI, Request
from sqlmodel import SQLModel, Session, Field, create_engine, select, or_, and_, col
from datetime import datetime, timedelta


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


db_url = 'sqlite:///database.db'
engine = create_engine(db_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


def create_heroes():

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", age=30)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age=16)
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America",
                  secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
     #    print("Creating heroes...", hero_1, hero_2, hero_3)
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)
        session.commit()
     #    session.refresh(hero_1)
     #    session.refresh(hero_2)
     #    session.refresh(hero_3)


def get_heroes():
    with Session(engine) as session:
     #    res1 = session.exec(select(Hero).where(Hero.name != 'Rusty-Man'))
     #    for hero in res1:
     #        print("Heroes found:", hero)
     #    res2 = session.exec(select(Hero).where(
     #        col(Hero.age) >= 35).where(col(Hero.age) <= 40))
     #    for hero in res2:
     #        print("Heroes found:", hero)
     #    res3 = session.exec(select(Hero).where(
     #        or_(Hero.name == 'Deadpond')))
     #    for hero in res3:
     #        print("Heroes found:", hero)
     #    print(f'res3:{res3.first()}')
     #    print(f'res3:{res3.one()}')
     #    res4 = session.get(Hero, 1222)
     #    print(f'res4:{res4}')

        res5 = session.exec(select(Hero).where(
            col(Hero.age) < 100).offset(20).limit(5))
        for hero in res5:
            print("Heroes found:", hero)


def update_heroes():
    with Session(engine) as session:
        hero = session.exec(select(Hero).where(Hero.name == "周睿好帅")).first()
        if hero:
            hero.name = "操他妈的周睿好帅"
            session.add(hero)
            session.commit()
            session.refresh(hero)


def delete_heroes():
    with Session(engine) as session:
        hero = session.get(Hero, 1)
        session.delete(hero)
        session.commit()
        print(f"Deleted hero with id 1: {hero}")


def init():
    create_db_and_tables()


#     create_heroes()
#     get_heroes()
# update_heroes()
delete_heroes()


@app.on_event("startup")
def on_startup():
    init()


if __name__ == "__main__":
    pass
