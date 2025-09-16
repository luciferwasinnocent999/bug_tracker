def login(client, username, password):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def test_create_task_as_developer(client, create_user):
    user = create_user("devuser", "testpass", role="developer")
    login(client, "devuser", "testpass")

    response = client.post('/tasks/create', data={
        'title': 'Fix Bug A',
        'description': 'Null pointer issue'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Task added successfully" in response.data


def test_create_task_as_admin_assigns_user(client, create_user):
    admin = create_user("adminuser", "testpass", role="admin")
    dev = create_user("devuser", "testpass", role="developer")

    login(client, "adminuser", "testpass")

    response = client.post('/tasks/create', data={
        'title': 'Critical Bug',
        'description': 'Server crash',
        'assigned_to': dev.id
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Task added successfully" in response.data