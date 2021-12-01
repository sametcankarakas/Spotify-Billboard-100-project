import json
import spotify
import requests
import base64
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


SPOTIFY_CLIENT_ID = "8d4f4ed4dd18467aa73a305a5c5078b5"
spotify_client_secret = "3204b34256884dfebdd5340f51d70007"
spotify_base_link = "https://api.spotify.com/v1/"
spotify_authorization_link = "https://accounts.spotify.com/api/token"
spotify_redirect_uri = "https://mumachine.com/callback/"
grant_type = 'client_credentials'
test_user = "https://open.spotify.com/user/31tfjsi2q2oqquaspl4izncmectq"
playlist_link = "https://api.spotify.com/v1/users/31tfjsi2q2oqquaspl4izncmectq/playlists"
me_link = "https://api.spotify.com/v1/me"
body_params = {'grant_type': grant_type}

playlist_body = {
    "name": "Test Playlist",
    "description": "Test description",
    "public": True
}


# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# response = requests.get(f"https://www.billboard.com/charts/hot-100/1990-07-05")
# response_text = response.text
#
# soup = BeautifulSoup(response_text, "html.parser")
# print(soup)
#
# titles = soup.find_all("h3", id="title-of-a-story")
#
#
# all_list = [title.getText().strip() for title in titles[3:103]]
# print(all_list)
#

response = requests.post(spotify_authorization_link, data=body_params, auth=(spotify_client_id, spotify_client_secret))
response.raise_for_status()
print(response.text)
token_raw = json.loads(response.text)
token = token_raw["access_token"]
print(token)
headers = {"Authorization": "Bearer {}".format(token)}
get_Header = {
    "Authorization": "Bearer" + token
}


# response_me = requests.get(me_link, auth=headers)
# response_me.raise_for_status()
# print(response_me.text)
# create_playlist = requests.post(url=playlist_link, auth=get_Header, data=playlist_body)
# create_playlist.raise_for_status()
# print(create_playlist.text)

me_response = requests.get(me_link, get_Header)
me_response.raise_for_status()
print(me_response.text)