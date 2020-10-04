## Find New Music


### What does this app do?

This app uses Spotify's api and enables you to search for artists and playlists.  The goal is to find new music using spotify’s api.

It allows user to sign up/login and log out. Each user will have a profile page where they can add playlists, edit them, delete them. To each playlist, they can search for new songs, add songs, and delete those songs.
  

### Resources
  
This app is built using Flask to build the routes, and postgres to build tables.

To use the spotify api, I found this [tutorial](https://www.youtube.com/watch?v=xdq6Gz33khQ) most useful. They use Jupyter, and on this app, I adapt their setup to this flask app. When setting up this app, you would need to add a file api.py with your spotify client_id and client_secret.


### To install this project

### Set up Virtual Environment

```console
python3 -m venv venv
$ source venv/bin/activate
```

### Create the Database

```console
createdb new_music
```

### Install necessary packages

```console
(venv) $ pip install -r requirements.txt
```



### Start the app

```console
flask run
```

### Run Tests

```console
createdb new_music-test
python -m unittest tests.py
```


### Explore database

```console
psql new_music
```

also you can test the models by inserting statements through ipython:
```console
ipython 
%run app.py
drop database: db.drop_all()
create a new database: db.create_all()
(update session key on app.py)
```



### Database Schema

The app will have 4 tables:

1. Users 
It will have an id, a username and a password. It will also have 2 methods to register and authenticate that will allow users to register or login to the site. The id will be the primary key.

2. Playlist:
It will have an id, a name. A user can have many playlists and these playlists can have many songs. It will be connected to other tables. 
It will be connected to “Users” because each user will only be seeing their own playlists. 
It will be connected to PlaylisSong because each playlist will hold many songs, and this table is where this connection comes together.

3. Song: 
It will have an id, a title, artists, spotify_id, album_name, album_image. All of these columns will be populated by the API. These songs will be added to a specific playlist to a specific user, which will be connected on the PlaylistSong table. Every time a user deletes a playlist, all of the songs in that specific playlist will be deleted from that playlist as well.

4. PlaylistSong 
This table will bring together  Song and Playlist so that we are able to build playlists with songs. These playlists are related to a specific user on the playlist table.


### Spotify API

To connect our app to spotify, we are going to work from: spotify.py. On this file we will create a class SpotifyAPI(object)

We will then go to their developer site and create an app on their site that will have a client ID and client secret.

Step 1: Get token With these two (client ID and client secret), one will be able to create a token to be able to authenticate with spotify api. For this, you will need the requests library from python. We use that token to make requests in the future. That token expires at some point. So it will be the equivalent of logging in to a session and staying logged in.

Authorization flows

On their website, there are 3 types of authorization flows. We need to look into one of the authorization flows in Spotify “Client Credentials Flow” that uses the Client ID and Secret Key to get the Access Token.

token_url : https://accounts.spotify.com/api/token The method is POST. Parameters that are required: token_data: grant_type: client_credentials

Token_header: base 64 encoded string (this step will require adding a base64 library to encode string)

So, the request will be:

response = requests.post(token_url, data= token_data, headers=token_headers)

This response will give us an access token.

Step Two: Create a search using spotify api

endpoint: https://api.spotify.com/v1/search method: GET Parameters: required parameter:Authorization (done on step 1) data: q’ for query “type”: “artist”

response = requests.get(endpoint, data=data, headers=headers)

