def test_register_and_login(client):
    # Registra um novo usuário
    register_response = client.post("/api/register", json={"username": "testuser", "password": "testpassword"})
    assert register_response.status_code == 200, register_response.text

    # Efetua login com o usuário criado
    login_response = client.post("/api/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, login_response.text
    token_data = login_response.json()
    assert "access_token" in token_data

    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria uma nova tarefa
    create_response = client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"}, headers=headers)
    assert create_response.status_code == 200, create_response.text
    task = create_response.json()
    task_id = task["id"]

    # Lista as tarefas
    list_response = client.get("/api/tasks", headers=headers)
    assert list_response.status_code == 200, list_response.text
    tasks = list_response.json()
    assert any(t["id"] == task_id for t in tasks)

    # Atualiza a tarefa
    update_response = client.put(f"/api/tasks/{task_id}", json={"title": "Updated Task", "status": "completed"}, headers=headers)
    assert update_response.status_code == 200, update_response.text
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["status"] == "completed"

    # Deleta a tarefa
    delete_response = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 200, delete_response.text
