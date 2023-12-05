from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Path
from pydantic import BaseModel, Field

router = APIRouter()


class Task(BaseModel):
    id: int | None = None
    title: str
    author: str
    description: str
    priority: int
    complete: bool
    created_on: datetime = datetime.utcnow()

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Title of the New Task",
                "author": "Jonathan Fernandes",
                "description": "Description of the new task",
                "priority": 1,
                "complete": False
            }
        }


def create_id(task: Task):
    task.id = 1 if len(TASKS) < 1 else TASKS[-1].id + 1
    return task


TASKS = [
    Task(**{
        "id": 1,
        "title": "Unit 8",
        "description": "In order to create more robust API's, we need to finish teaching Unit 8",
        "author": "Jonathan Fernandes",
        "priority": 5,
        "complete": False
    }),
    Task(**{
        "id": 2,
        "title": "Buy Flowers",
        "description": "Since Mrs. Fernandes has been so mean to her students, I will try to cheer her up",
        "author": "Jonathan Fernandes",
        "priority": 2,
        "complete": False
    })
]


@router.get("")
async def get_all_tasks():
    return TASKS


@router.post("")
async def create_task(task_data: Task):
    new_task = Task(**task_data.model_dump())
    TASKS.append(create_id(new_task))
    return new_task


@router.get("/{task_id}")
async def get_task_by_id(task_id: int):
    for task in TASKS:
        if task_id == task.id:
            return task
    return {"msg": f"Task not found with id#{task_id}"}


@router.put("/{task_id}")
async def update_task_by_id(task_id: int, task_data: Task):
    task_updated = False
    for index in range(len(TASKS)):
        if task_id == TASKS[index].id:
            TASKS[index].title = task_data.title
            TASKS[index].author = task_data.author
            TASKS[index].description = task_data.description
            TASKS[index].priority = task_data.priority
            TASKS[index].complete = task_data.complete
            task_updated = True
    if not task_updated:
        return {"msg": f"Task not found with id#{task_id}"}


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(task_id: int = Path(gt=0)):
    task_deleted = False
    for index in range(len(TASKS)):
        if task_id == TASKS[index].id:
            TASKS.pop(index)
            task_deleted = True
    if not task_deleted:
        return {"msg": f"Task not found with id#{task_id}"}
