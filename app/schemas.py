from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"

class TaskBase(BaseModel):
    title: str = Field(..., example="Comprar leite", description="Título da tarefa")
    description: Optional[str] = Field(None, example="Comprar leite integral no supermercado", description="Descrição da tarefa")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Comprar leite atualizado", description="Novo título da tarefa")
    description: Optional[str] = Field(None, example="Atualizar descrição", description="Nova descrição da tarefa")
    status: Optional[TaskStatus] = Field(None, example="completed", description="Status da tarefa")

class Task(TaskBase):
    id: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    status: TaskStatus

    class Config:
        orm_mode = True  # Ou, se preferir, 'from_attributes = True' para Pydantic V2

class UserBase(BaseModel):
    username: str = Field(..., example="usuario_teste", description="Nome de usuário")

class UserCreate(UserBase):
    password: str = Field(..., example="StrongP@ssw0rd!", description="Senha do usuário")

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str = Field(..., example="jwt_token_string")
    token_type: str = Field(..., example="bearer")

class TokenData(BaseModel):
    username: Optional[str] = None
