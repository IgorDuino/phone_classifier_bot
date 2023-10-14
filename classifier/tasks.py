from dtb.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def classify_number(phone_number: str) -> None:
    pass
