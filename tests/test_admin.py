def login(client, username, password):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def test_admin_dashboard_lists_users(client, create_user):
    admin = create_user("adminuser", "testpass", role="admin")
    dev1 = create_user("dev1", "testpass")
    dev2 = create_user("dev2", "testpass")

    login(client, "adminuser", "testpass")

    response = client.get('/admin')
    assert response.status_code == 200
    assert b"adminuser" in response.data
    assert b"dev1" in response.data
    assert b"dev2" in response.data


def test_developer_cannot_access_admin(client, create_user):
    dev = create_user("devuser", "testpass", role="developer")
    login(client, "devuser", "testpass")

    response = client.get('/admin', follow_redirects=True)
    assert response.status_code == 200
    assert b"Access denied" in response.data