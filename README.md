# GrupoMoura Task Manager API

## Descrição

Este é um sistema de gerenciamento de tarefas com autenticação utilizando FastAPI, JWT e PostgreSQL.  
O projeto está dockerizado para facilitar o desenvolvimento e a implantação.

## Funcionalidades

- Registro e login de usuários com autenticação JWT.
- Criação, visualização, atualização e exclusão de tarefas.
- Cada tarefa possui título, descrição, data de criação, data de conclusão (opcional) e status (pendente ou concluída).

## Tecnologias Utilizadas

- Python, FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Docker e Docker Compose

## Como Executar o Projeto

1. **Clone o repositório:**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd grupo_moura

2. **Suba os containers com Docker Compose:**
   docker-compose up --build


3.  **Acesse a API:**

    Documentação interativa (Swagger): http://localhost:8000/docs
    Redoc: http://localhost:8000/redoc