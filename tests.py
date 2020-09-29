import os
from unittest import TestCase
from flask import session




# Use test database and don't clutter tests with SQL
os.environ['DATABASE_URL'] = "postgresql:///new_music-test"
from app import app
from models import db, connect_db, Playlist, User, PlaylistSong
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///new_music-test'
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
  def setUp(self):
    """Create test client, add sample data."""

    db.drop_all()
    db.create_all()

    self.client = app.test_client()

    self.testuser = User.register(username="testuser",
                                pwd="testuser")
    self.testuser_id = 1
    self.testuser.id = self.testuser_id

    db.session.commit()

  def tearDown(self):
    #  resp is being set to be a class that has all the attributes of the tearDown() built in unittest method.
    #  res runs the tearDown, which means it will happen after each test.

    resp = super().tearDown()
    db.session.rollback()
    return resp


  def test_redirectHomepage(self):
    with app.test_client() as client:
      res = client.get('/', follow_redirects=True)
  

  def test_user_model(self):
    """Does basic model work?"""

    u = User(
        username="testuser",
        password="HASHED_PASSWORD"
    )

    db.session.add(u)
    db.session.commit()

    # User should have no messages & no followers
    self.assertEqual((u.id), 1)

  def test_playlist_model(self):
    u = User(
        username="testuser",
        password="HASHED_PASSWORD"
    )

    p = Playlist(name='Spring', user_id=1)
    db.session.add(p)
    db.session.add(u)
    db.session.commit()

    # User should have id 1, and 1 playlist
    self.assertEqual((p.user_id), 1)
    self.assertEqual(len(u.playlists), 1)

  def test_session_info_set(self):
    with app.test_client() as client:
      # Any changes to session should go in here:
      u = User(
        username="testuser",
        password="HASHED_PASSWORD"
      )
      db.session.add(u)
      db.session.commit()
      with client.session_transaction() as change_session:
          change_session['user_id'] = 1

      # Now those changes will be in Flask's `session`
      resp = client.get("/")
      self.assertEqual(resp.location, "http://localhost/register")
      self.assertEqual(resp.status_code, 302)
      self.assertEqual(session['user_id'], 1)


  # def test_session_info(self):
  #   with app.test_client() as client:
  #     u = User(
  #       username="testuser",
  #       password="HASHED_PASSWORD"
  #     )
  #     db.session.add(u)
  #     db.session.commit()
  #     resp = client.get("/")


  #     self.assertEqual(resp.status_code, 302)
  #     self.assertEqual(session['user_id'], 1)

  # def test_invalid_username_signup(self):
  #       user = User.register("test@test.com", "password")
  #       uid = 1
  #       user.id = uid
  #       session['user_id'] = request.form["user_id"]
  #       self.assertEqual((user.id), 1)

  # def test_logout(self):
  #   with app.test_client() as client:
  #     res = client.get('/logout', follow_redirects=True)

  # def test_profile_page(self):
  #   with app.test_client() as client:


  # def test_login(self):
  #   with app.test_client() as client:
  #     resp = client.post('/register', data={'user':'thur', 'password': 'thur', 'confirm': 'thur'})
  #     html = resp.get_data(as_text=True)
  #     self.assertIn('Hello thur', html)


  # def login(client, username, password):
  #   return client.post('/login', data=dict(
  #       username=username,
  #       password=password
  #   ), follow_redirects=True)


  # def logout(client):
  #   return client.get('/logout', follow_redirects=True)

  # def test_login_logout(client):
  #   """Make sure login and logout works."""

  #   rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
  #   assert b'You were logged in' in rv.data

  #   rv = logout(client)
  #   assert b'You were logged out' in rv.data

  #   rv = login(client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
  #   assert b'Invalid username' in rv.data

  #   rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
  #   assert b'Invalid password' in rv.data

  # def test_client_login(self):
  #   with app.test_client() as client:
  #     resp = client.post('/register', data={'user':'thur', 'password': 'thur', 'confirm': 'thur'})
  #     html = resp.get_data(as_text=True)
  #     self.assertIn('Hello thur', html)

      

      # # self.assertEqual(res.status_code, 200)


      # # if session['user_id']:
      # self.assertEqual(session['user_id'], 1)