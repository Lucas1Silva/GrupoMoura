from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from .. import models, schemas
from sqlalchemy.future import select

async def create_task(db: AsyncSession, task_data: schemas.TaskCreate, user_id: int):
    new_task = models.Task(**task_data.dict(), owner_id=user_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

async def get_tasks(db: AsyncSession, user_id: int, skip: int, limit: int):
    result = await db.execute(select(models.Task).filter(models.Task.owner_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()

async def get_task(db: AsyncSession, task_id: int, user_id: int):
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id))
    return result.scalars().first()

async def update_task(db: AsyncSession, task_id: int, task_update: schemas.TaskUpdate, user_id: int):
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id))
    task = result.scalars().first()
    if not task:
        return None
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        if task_update.status == models.TaskStatus.completed and task.status != models.TaskStatus.completed:
            task.completed_at = datetime.utcnow()
        task.status = task_update.status
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task_id: int, user_id: int):
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id))
    task = result.scalars().first()
    if not task:
        return False
    await db.delete(task)
    await db.commit()
    return True
