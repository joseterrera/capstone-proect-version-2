from flask import Flask, render_template, redirect, session, flash, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import db, connect_db, Playlist, Song, PlaylistSong, User
from forms import  PlaylistForm, RegisterForm, LoginForm, DeleteForm, SearchSongsForm
from spotify import spotify
from helpers import pick, pick_from_list, first
import json
import os
from api import CLIENT_ID, CLIENT_SECRET

my_spotify_client = spotify.Spotify(CLIENT_ID, CLIENT_SECRET)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///new_music')
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///new_music"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'abc123456')

connect_db(app)
# db.create_all()


toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



@app.route("/")
def homepage():
    """Show homepage with links to site areas."""
    # raise 'here'
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""
    if "user_id" in session:
        return redirect(f"/users/profile/{session['user_id']}")

    form = RegisterForm()
    name = form.username.data
    pwd = form.password.data
    existing_user_count = User.query.filter_by(username=name).count()
    if existing_user_count > 0:
        flash("User already exists")
        return redirect('/login')

    if form.validate_on_submit():
        user = User.register(name, pwd)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        # on successful login, redirect to profile page
        return redirect(f"/users/profile/{user.id}")
    else:
        return render_template("/users/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()
    if not form.validate_on_submit():
        return render_template("users/login.html", form=form)
    # otherwise
    name = form.username.data
    pwd = form.password.data
    # authenticate will return a user or False
    user = User.authenticate(name, pwd)

    if not user:
        return render_template("users/login.html", form=form)
    # otherwise

    form.username.errors = ["Bad name/password"]
    my_spotify_client.perform_auth()
    session["spotify_access_token"] = my_spotify_client.access_token
    session["spotify_access_token_expires"] = my_spotify_client.access_token_expires
    session["spotify_access_token_did_expire"] = my_spotify_client.access_token_did_expire
    session["user_id"] = user.id  
    return redirect(f"/users/profile/{user.id}")



@app.route("/users/profile/<int:id>",  methods=["GET", "POST"])
def profile(id):
    """Example hidden page for logged-in users only."""

    # raise 'here'
    if "user_id" not in session or id != session['user_id']:
        flash("You must be logged in to view!")
        return redirect("/login")
    else:
        id = session["user_id"]
        user = User.query.get_or_404(id)
        form = PlaylistForm()
        playlists = Playlist.query.filter_by(user_id=id).all()
        if form.validate_on_submit(): 
            name = form.name.data
            new_playlist = Playlist(name=name, user_id=session['user_id'])
            db.session.add(new_playlist)
            db.session.commit()
            playlists.append(new_playlist)
            return redirect(f"/users/profile/{id}")
        return render_template("users/profile.html", playlists=playlists, form=form, user=user)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("user_id")
    return redirect("/login")


@app.route("/playlists/<int:playlist_id>", methods=['POST', 'GET'])
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    if "user_id" not in session or  playlist.user_id != session['user_id']:
        flash("You must be logged in to view!")
        return redirect("/login")
    
    songs = PlaylistSong.query.filter_by(playlist_id=playlist_id)
    form = request.form
    if request.method == 'POST' and form['remove'] and form['song']:
        song_id = form['song']
        song_to_delete = PlaylistSong.query.get(song_id)
        db.session.delete(song_to_delete)
        db.session.commit()
    return render_template("playlist/playlist.html", playlist=playlist, songs=songs)


@app.route('/playlists/<int:playlist_id>/search', methods=["GET", "POST"])
def show_form(playlist_id):
    """Show form that searches new form, and show results"""
    playlist = Playlist.query.get(playlist_id)
    play_id  = playlist_id
    form = SearchSongsForm()
    resultsSong = []
    checkbox_form = request.form
    
    # search form
    if form.validate_on_submit() and checkbox_form['form'] == 'search_songs': 
        track_data = form.track.data
        api_call_track = my_spotify_client.search(track_data,'track')   

        for item in api_call_track['tracks']['items']:
            images = [ image['url'] for image in item['album']['images'] ]
            artists = [ artist['name'] for artist in item['artists'] ]
            urls = item['album']['external_urls']['spotify']
            resultsSong.append({
                'title' : item['name'],
                'spotify_id': item['id'],
                'album_name': item['album']['name'], 
                'album_image': first(images,''),
                'artists': ", ".join(artists),
                'url': urls
            })

    list_of_songs_spotify_id_on_playlist = []
    for song in playlist.songs:
      list_of_songs_spotify_id_on_playlist.append(song.spotify_id)
    song_set = set(list_of_songs_spotify_id_on_playlist)
    
    if 'form' in checkbox_form and checkbox_form['form'] == 'pick_songs':

        list_of_picked_songs = checkbox_form.getlist('track')
        # map each item in list of picked songs
        jsonvalues = [ json.loads(item) for item in  list_of_picked_songs ]

        for song in jsonvalues:
          # print(song['spotify_id'])
          if song['spotify_id'] not in song_set:
            raise('here')

            for item in jsonvalues:
                title = item['title']
                spotify_id = item['spotify_id']
                album_name = item['album_name']
                album_image = item['album_image']
                artists = item['artists']
                # print(title)
                new_songs = Song(title=title, spotify_id=spotify_id, album_name=album_name, album_image=album_image, artists=artists)
                db.session.add(new_songs)
                db.session.commit()

                playlist_song = PlaylistSong(song_id=new_songs.id, playlist_id=playlist_id)
                db.session.add(playlist_song)
                db.session.commit()
        # raise 'here'    
        return redirect(f'/playlists/{playlist_id}')



    def serialize(obj):
        return json.dumps(obj)
    return render_template('song/search_new_songs.html', playlist=playlist, form=form, resultsSong=resultsSong, serialize=serialize)

@app.route("/playlists/<int:playlist_id>/update", methods=["GET", "POST"])
def update_playlist(playlist_id):
    """Show update form and process it."""

    playlist = Playlist.query.get(playlist_id)

    if "user_id" not in session or playlist.user_id != session['user_id']:
        flash("You must be logged in to view!")
        return redirect("/login")

    form = PlaylistForm(obj=playlist)

    if form.validate_on_submit():
        playlist.name = form.name.data
        db.session.commit()
        return redirect(f"/users/profile/{session['user_id']}")
    
    return render_template("/playlist/edit.html", form=form, playlist=playlist)



@app.route("/playlists/<int:playlist_id>/delete", methods=["POST"])
def delete_playlist(playlist_id):
    """Delete playlist."""

    playlist = Playlist.query.get(playlist_id)
    if "user_id" not in session or playlist.user_id != session['user_id']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(playlist)
        db.session.commit()

    return redirect(f"/users/profile/{session['user_id']}")
