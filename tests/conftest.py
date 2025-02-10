import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from sqlalchemy.orm import sessionmaker

# Cria uma sessão de teste (pode ser a mesma que a do ambiente, para simplificar)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def client():
    # Setup: cria as tabelas
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Teardown: remove as tabelas
    Base.metadata.drop_all(bind=engine)
