# """User model tests."""

# # run these tests like:
# #
# #    python -m unittest test_user_model.py


# import os
# from unittest import TestCase

# from models import db, User, Playlist

# # BEFORE we import our app, let's set an environmental variable
# # to use a different database for tests (we need to do this
# # before we import our app, since that will have already
# # connected to the database

# os.environ['DATABASE_URL'] = "postgresql:///new_music-test"


# # Now we can import app

# from app import app

# # Create our tables (we do this here, so we only create the tables
# # once for all tests --- in each test, we'll delete the data
# # and create fresh new clean test data

# db.create_all()


# class UserModelTestCase(TestCase):
#     """Test views for messages."""

#     def setUp(self):
#         """Create test client, add sample data."""

#         User.query.delete()
#         Playlist.query.delete()

#         self.client = app.test_client()

#     def test_user_model(self):
#         """Does basic model work?"""

#         u = User(
#             username="testuser",
#             password="HASHED_PASSWORD"
#         )

#         p = Playlist(
#           name="One playlist"
#         )

#         db.session.add(u)
#         db.session.add(p)
#         db.session.commit()

#         # User should have no messages & no followers
#         self.assertEqual(u.id, 1)
#         # self.assertEqual(len(p), 1)


import os
from unittest import TestCase
from flask import session

from models import db, Playlist, User



# Use test database and don't clutter tests with SQL
# os.environ['DATABASE_URL'] = "postgresql:///new_music-test"
from app import app
from models import db, connect_db, Playlist, User
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///new_music-test'
# app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class musicAppTestCases(TestCase):
  """Tests for views of API"""
  # with app.test_client() as client:
  #   import pdb
  #   pdb.set_trace() 
  def test_redirectHomepage(self):
    with app.test_client() as client:
      res = client.get('/', follow_redirects=True)


  def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


  def logout(client):
    return client.get('/logout', follow_redirects=True)

  def test_login_logout(client):
    """Make sure login and logout works."""

    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
    assert b'Invalid username' in rv.data

    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data

  # def test_client_login(self):
  #   with app.test_client() as client:
  #     resp = client.post('/register', data={'user':'thur', 'password': 'thur', 'confirm': 'thur'})
  #     html = resp.get_data(as_text=True)
  #     self.assertIn('Hello thur', html)

      

      # # self.assertEqual(res.status_code, 200)


      # # if session['user_id']:
      # self.assertEqual(session['user_id'], 1)