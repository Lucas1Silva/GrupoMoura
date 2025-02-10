# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from app.database import engine, Base
from app.routers import auth, tasks
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from app.logger import logger

# Cria as tabelas do banco de dados, se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="API para gerenciar tarefas com autenticação JWT"
)

# Configuração de CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    # Adicione outros origins conforme necessário
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

# Inclusão dos roteadores
app.include_router(auth.router)
app.include_router(tasks.router)

logger.info("Application startup complete.")
