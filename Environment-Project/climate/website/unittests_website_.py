import unittest
import pytest
from .__init__ import create_app

flask_app = create_app()


@pytest.fixture()
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


# class TestLandingPage(unittest.TestCase):
def test_landing_page(app, client):
    response = client.get('/')
    assert response.status_code == 200

#login tests
#class login(unittest.TestCase):

#Ensure that login page loads correctly
def test_login_loads(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_correct_login(client):
    response = client.post('/login',
    data=dict(email="jj@jj.com", password="Jack123"),
    follow_redirects=True)
    assert(b'Welcome' in response.data)

#ensure that incorrect login gets 'try again' message

def test_incorrect_login(client):
    response = client.post('/login',
    data=dict(email="jj@jj.comx", password="Jack123x"),
    follow_redirects=True)
    assert(b'try again' in response.data)

#ensure that trying to navigate to logged in page without logging in - invites user to login
def test_logged_in_without_authentication(client):
    response = client.get('/logged_in', follow_redirects=True)
    assert (b'login' in response.data)
#test logout
#class TestLogout(unittest.TestCase):

#test if logging out results in logout message
def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert (b'logged out' in response.data)

#check if save searches correctly inserted into database

#test signup page
#class Testsignup(unittest.TestCase):

#test if correct sign up result in account created message
def test_incorrect_sign_up(client):
    response = client.post('/sign_up',
    data=dict(email="xx@xx.com", first_name="Xavier", password1="Xavier123", password2="Xavier123"),
    follow_redirects=True)
    assert(b'success' in response.data)


#test if error flashed when email exists
def test_email_exists_sign_up(client):
    response = client.post('/sign_up',
    data=dict(email="jj@jj.com", first_name="Xavier", password1="Xavier123", password2="Xavier123"),
    follow_redirects=True)
    assert(b'exists' in response.data)


if __name__ == '__main__':
    unittest.main()
