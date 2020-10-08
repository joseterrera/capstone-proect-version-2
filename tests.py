import os
from unittest import TestCase
from flask import session

# Use test database and don't clutter tests with SQL
os.environ['DATABASE_URL'] = "postgresql:///new_music-test"
from app import app
from models import db, connect_db, Playlist, User, PlaylistSong
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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
      resp = client.get("/")
      self.assertEqual(resp.location, "http://localhost/register")
      self.assertEqual(resp.status_code, 302)
      self.assertEqual(session['user_id'], 1)
