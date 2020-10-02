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
