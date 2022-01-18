import requests
import spotipy
import spotipy.util as util

# Getting auth token
AUTH_URL = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': '0c73fd524c97444da6dcf18cb94eabd3',
    'client_secret': '5d35e5da6b804c76aeaa8c936cb4487f',
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}
#spotipy auth setup
scope = 'playlist-modify-private'
token = util.prompt_for_user_token('laser8000', scope,
                                client_id='0c73fd524c97444da6dcf18cb94eabd3',
                                client_secret='5d35e5da6b804c76aeaa8c936cb4487f',
                                redirect_uri='http://localhost:8080')

# API endpoints to get all the songs
g1 = "https://api.spotify.com/v1/playlists/3ViW4euqk6opmrgEZV3sEv/tracks?limit=100"
g2 = "https://api.spotify.com/v1/playlists/3ViW4euqk6opmrgEZV3sEv/tracks?offset=100&limit=100"
g3 = "https://api.spotify.com/v1/playlists/3ViW4euqk6opmrgEZV3sEv/tracks?offset=200&limit=100"
gets = [g1, g2, g3]

# Lists to add the URIs to
s1 = []
s2 = []
s3 = []

# sort playlist into separate lists based on artists
for url in gets:
    response = requests.get(url, headers=headers)
    r = response.json()
    for item in r['items'] :
        uri = item['track']['uri']
        id = item['track']['id']
        artists = [s['name'].lower() for s in item['track']['artists']]
        if any(name in open('list1.txt').read() for name in artists):
            s1.append(id)
        elif any(name in open('list2.txt').read() for name in artists):
            s2.append(id)
        elif any(name in open('list3.txt').read() for name in artists):
            s3.append(id)
        else:
            print("could not find", item['track']['name'], "by", artists)

print(len(s1) + len(s2) + len(s3), "songs found")
print(len(s1), "songs to playlist 1")
print(len(s2), "songs to playlist 2")
print(len(s3), "songs to playlist 3")

# URIs for the new playlists
p1 = '3uWNxJeK7L59G4IknM2rx5'
p2 = '6zk5ID9HRJGFiMW63EY8dd'
p3 = '6eJvrcg8Phtk6zpflcp33E'

# adding songs to each playlist
if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    sp.user_playlist_add_tracks('laser8000', p1, s1)
    sp.user_playlist_add_tracks('laser8000', p2, s2)
    sp.user_playlist_add_tracks('laser8000', p3, s3)