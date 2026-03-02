from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlmodel import Session, SQLModel, Field, create_engine
from ..db import get_session

router = APIRouter()


class ReminderBase(SQLModel):
    title: str
    description: str | None = None
    remind_time: str
    # user_id: int


class Reminder(ReminderBase, table=True):
    id: int = Field(default=None, primary_key=True)


@router.post('/remind', tags=["remind"], summary="Create a reminder", response_description="The created reminder")
async def create_reminder(form_data: ReminderBase, session: Annotated[Session, Depends(get_session)]):
    de_reminder = Reminder.model_validate(form_data)
    session.add(de_reminder)
    session.commit()
    session.refresh(de_reminder)
    return de_reminder
