import requests
import spotipy
import spotipy.util as util

# Getting auth token
AUTH_URL = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': 'YOUR-CLIENT-ID-HERE',
    'client_secret': 'YOUR-CLIENT-SECRET-ID-HERE',
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}
#spotipy auth setup
scope = 'playlist-modify-private'
token = util.prompt_for_user_token('laser8000', scope,
                                client_id='YOUR-CLIENT-ID-HERE',
                                client_secret='YOUR-CLIENT-SECRET-ID-HERE',
                                redirect_uri='http://localhost:8080')

# API endpoints to get all the songs
g1 = "https://api.spotify.com/v1/playlists/3ViW4euqk6opmrgEZV3sEv/tracks?limit=100"
g2 = "https://api.spotify.com/v1/playlists/3ViW4euqk6opmrgEZV3sEv/tracks?offset=100&limit=100"
g3 = "https://api.spotify.com/v1/playlists/3ViW4euqk6opmrgEZV3sEv/tracks?offset=200&limit=100"
gets = [g1, g2, g3]

# List of artists to sort by
a1 = ["i prevail", "parkway drive", "the ghost inside", "alexisonfire", "hatebreed", "knocked loose", "sleeping with sirens", "bleeding through",
        "born of osiris", "carnifex", "crown the empire", "lorna shore", "polyphia", "stick to your guns", "suicide silence", "the acacia strain",
        "the black dahlia murder", "veil of maya", "angelmaker", "chamber", "distant", "dropout kings", "escape the fate", "fire from the gods",
        "gideon", "he is legend", "if i die first", "jynx", "left to suffer", "new years day", "omerta", "signs of the swarm", "spite",
        "the callous daoboys", "the word alive", "traitors", "unitytx", "upon a burning body", "volumes"]
a2 = ["blackbear", "simple plan", "sum 41", "3oh!3", "grandson", "the maine", "against the current", "maggie lindemann", "nothing,nowhere.",
        "poorstacy", "set it off", "stand atlantic", "belmont", "bilmuri", "blackstarkids", "cemetery sun", "chad tepper", "concrete castles",
        "first and forever", "girlfriends", "heart attack man", "john harvie", "keep flying", "lil aaron", "point north", "tramp stamps",
        "tyler posey", "with confidence"]
a3 = ["2 chainz", "rae sremmurd", "trippie redd", "tyga", "24kgoldn", "$not", "princess nokia", "waka flocka flame", "bankrol hayden", "cochise",
        "idk", "jasiah", "lil darkie", "paris texas", "10k.caash", "22gz", "boobie lootaveli", "father", "freddie dredd", "haarper", "kah-lo",
        "kay flock", "ken car$on", "kidd kenn", "kodoku", "kxllswxtch", "lancey foux", "lil gnar", "matt ox", "midwxst", "oliver francis", 
        "omenxiii", "ppcocaine", "rich dunk", "robb bank$", "savage ga$p", "ssgkobe", "stunna 4 vegas", "travie mccoy", "yng martyr"]

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
        if any(name in a1 for name in artists):
            s1.append(id)
        elif any(name in a2 for name in artists):
            s2.append(id)
        elif any(name in a3 for name in artists):
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