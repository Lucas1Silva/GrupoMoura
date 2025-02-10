from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Schemas para usuários
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True

# Schemas para token (JWT)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Schemas para tarefas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # "pending" ou "completed"

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    status: str
    owner_id: int

    class Config:
        orm_mode = True
