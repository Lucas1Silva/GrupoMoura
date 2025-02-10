from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, database, models, auth
from ..services import task_service

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)

@router.get("/", response_model=list[schemas.Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    tasks = await task_service.get_tasks(db, current_user.id, skip, limit)
    return tasks

@router.post("/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_task = await task_service.create_task(db, task, current_user.id)
    return new_task

@router.get("/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task = await task_service.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task_update: schemas.TaskUpdate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    updated_task = await task_service.update_task(db, task_id, task_update, current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", response_model=dict)
async def delete_task(task_id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    result = await task_service.delete_task(db, task_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

# Exemplo de endpoint com Background Tasks (por exemplo, simulação de envio de email)
@router.post("/send_email", response_model=dict)
async def send_email(background_tasks: BackgroundTasks, email: str):
    # Adiciona a tarefa de envio de email para execução em background
    background_tasks.add_task(dummy_email_sender, email)
    return {"detail": f"Email sending initiated to {email}"}

async def dummy_email_sender(email: str):
    import asyncio
    # Simula uma operação demorada (por exemplo, envio de email)
    await asyncio.sleep(5)
    print(f"Email sent to {email}")
