from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas

def create_task(db: Session, task_data: schemas.TaskCreate, user_id: int):
    new_task = models.Task(**task_data.dict(), owner_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db: Session, user_id: int, skip: int, limit: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int, user_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()

def update_task(db: Session, task_id: int, task_update, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()
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
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True
