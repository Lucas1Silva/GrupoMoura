from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.TaskOut])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tasks = crud.get_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.create_task(db, task=task, owner_id=current_user.id)

@router.get("/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = crud.get_task(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task_db = crud.get_task(db, task_id=task_id, owner_id=current_user.id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        updated_task = crud.update_task(db, task_db=task_db, task_update=task_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_task

@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task_db = crud.get_task(db, task_id=task_id, owner_id=current_user.id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task_db=task_db)
    return {"detail": "Task deleted successfully"}
