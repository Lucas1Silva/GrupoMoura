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
4.  **Testes do projeto**
    docker-compose run --rm app pytest
5.  * DURANTE OS TESTES, PARA OBTENÇÃO DO BEARER TOKEN **
* curl -X 'POST' \
  'http://localhost:8000/api/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=usuario_teste&password=senha123'


## Arquitetura do Projeto

Este projeto segue uma arquitetura modular em camadas, que promove uma clara separação de responsabilidades e facilita a manutenção, testes e evolução do sistema. A estrutura adotada é a seguinte:

    API (Routers/Controllers):
        Os endpoints são definidos nos arquivos dentro de app/routers/ (por exemplo, auth.py e tasks.py).
        Esses arquivos são responsáveis por receber as requisições HTTP, validar os dados (usando schemas do Pydantic) e encaminhar as solicitações para a camada de serviços.

    Serviços (Business Logic):
        A lógica de negócio é isolada nos arquivos dentro de app/services/ (por exemplo, user_service.py e task_service.py).
        Essa camada realiza operações de criação, atualização, consulta e deleção de dados sem misturar a lógica de negócio com a interface da API.

    Acesso a Dados (Models e Database):
        Os modelos de dados (entidades) são definidos em app/models.py utilizando SQLAlchemy.
        A configuração e gerenciamento da conexão com o banco de dados (PostgreSQL) são realizados em app/database.py.

    Validação e Esquemas:
        Os schemas (definidos em app/schemas.py) são usados para validar e serializar os dados que entram e saem da API.

    Infraestrutura e Configuração:
        O projeto utiliza Docker e Docker Compose para facilitar o ambiente de desenvolvimento e produção.
        As variáveis de ambiente são gerenciadas com o python-dotenv (arquivo .env), garantindo que configurações sensíveis, como a URL do banco de dados e a chave secreta para JWT, sejam facilmente configuráveis.
        Implementamos middlewares para CORS, rate limiting (usando o SlowAPI) e logging para monitorar a aplicação.