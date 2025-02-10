from fastapi import FastAPI
from app.database import engine, Base
from app.routes import users, tasks

app = FastAPI(title="GrupoMoura Task Manager API")

# Cria as tabelas (para produção, considere usar migrações)
Base.metadata.create_all(bind=engine)

# Inclui os routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/")
def root():
    return {"message": "Welcome to GrupoMoura Task Manager API"}
