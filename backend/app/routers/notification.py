from fastapi import APIRouter, BackgroundTasks, Depends
from typing import Annotated
from pathlib import Path

router = APIRouter(
    prefix='/notifications',
    tags=["notifications"],
)


LOG_FILE = Path(__file__).resolve().parents[2] / "log.txt"


def write_notification(email: str, msg=''):
    with open(LOG_FILE, mode='a', encoding='utf-8') as email_file:
        content = f"notification for {email}: {msg}"
        email_file.write(content)


def get_query(bg_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        bg_tasks.add_task(write_notification,
                          email="admin@example.com", msg=message)
    return q


@router.post('/send/{email}')
async def send_notification(email: str, bg_tasks: BackgroundTasks, q: Annotated[str | None, Depends(get_query)]):
    bg_tasks.add_task(write_notification, email, msg="some notification")
    return {"message": "Notification sent in the background"}
