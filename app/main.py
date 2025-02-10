import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

from app.database import engine, Base
from app.routers import auth, tasks
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.logger import logger

app = FastAPI(
    title="Task Management API",
    description="API para gerenciar tarefas com autenticação JWT (Async)"
)

# Configuração de CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting com SlowAPI
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Limite de requisições excedido. Tente novamente mais tarde."}
    )

# Evento de startup assíncrono para criar as tabelas no banco de dados
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Application startup complete.")

# Inclusão dos routers
app.include_router(auth.router)
app.include_router(tasks.router)
