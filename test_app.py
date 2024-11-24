import pytest
from app import app, db, User
from flask import Flask
from flask_login import login_user

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test database
    app.config['TESTING'] = True
    app.secret_key = 'supersecretkey'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create test database tables
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 302  # Should redirect to login page
    assert b'Registration successful!' in response.data

def test_login(client):
    # First, register the user
    client.post('/register', data={
        'username': 'testuser',
        'password': 'password123',
        'confirm_password': 'password123'
    })

    # Then, log in with the credentials
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 302  # Should redirect to the protected page
    assert b'Hello, testuser!' in response.data

def test_invalid_login(client):
    response = client.post('/login', data={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 302  # Should redirect back to the login page
    assert b'Invalid username or password!' in response.data
