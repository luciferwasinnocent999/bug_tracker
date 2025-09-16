def test_register_user(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass',
        'role': 'developer'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Registration successful" in response.data


def test_login_user(client, create_user):
    create_user("loginuser", "testpass")

    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'testpass'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data