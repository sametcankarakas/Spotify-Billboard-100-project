import os
import json
import requests
import base64
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_base_link = "https://api.spotify.com/v1/"
spotify_authorization_link = "https://accounts.spotify.com/api/token"
spotify_redirect_uri = "https://mumachine.com/callback/"
grant_type = 'client_credentials'
test_user = os.environ['test_user']
playlist_link = os.environ['playlist_link']
me_link = "https://api.spotify.com/v1/me"
body_params = {'grant_type': grant_type}

playlist_body = {
    "name": "Test Playlist",
    "description": "Test description",
    "public": True
}


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
response_text = response.text

soup = BeautifulSoup(response_text, "html.parser")

titles = soup.find_all("h3", id="title-of-a-story")


all_list = [title.getText().strip() for title in titles[3:103]]
print(all_list)


# response = requests.post(spotify_authorization_link, data=body_params, auth=(spotify_client_id, spotify_client_secret))
# response.raise_for_status()
# print(response.text)
# token_raw = json.loads(response.text)
# token = token_raw["access_token"]
# print(token)
# headers = {"Authorization": "Bearer {}".format(token)}
# get_Header = {
#     "Authorization": "Bearer" + token
# }



#getting token with authorization info...
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://127.0.0.1:5500/",
        client_id= SPOTIFY_CLIENT_ID,
        client_secret= SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


create_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, collaborative=False, description="yo its description")
print(create_playlist["id"])

song_uris = []
year = date.split("-")[0]
for song in all_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(song_uris)

playlist_add = sp.playlist_add_items(playlist_id=create_playlist["id"], items=song_uris, position=None)