import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import random

DEVICE_ID="9406b4de41523bd2e8c232cf4e588df16b71333f"
CLIENT_ID="365ff2fe8b054874aa2bcb01926a134b"
CLIENT_SECRET="b5e702306c004495b5cb663da1296973"

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri="http://localhost:8080",
                                                scope="user-read-playback-state,user-modify-playback-state"))


# Transfer playback to the Raspberry Pi if music is playing on a different device
sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
sp.shuffle(True)
#playlist1_uri = 'spotify:playlist:0vvXsWCC9xrXsKd4FyS8kM'
#sp.start_playback(device_id=DEVICE_ID, context_uri=playlist1_uri, offset={"position":0})

playlist1 = []
results = sp.playlist_items(playlist_id='0vvXsWCC9xrXsKd4FyS8kM')
for i, track in enumerate(results['items']):
    try:
        entry = {'name': track['track']['name'], 'uri': track['track']['uri']}
        playlist1.append(entry)

    except TypeError:
        None

volume = 100
sp.shuffle(True)
sp.start_playback(device_id=DEVICE_ID, uris=[playlist1[random.randint(0,len(playlist1))]['uri']])
sleep(10)

for i in range(0, 10000):
    if(i%5 == 0):
        volume -= 2
        sp.volume(volume)
    if(volume == 0):
        break

sp.start_playback(device_id=DEVICE_ID, uris=[playlist1[random.randint(0,len(playlist1))]['uri']])
for i in range(0, 10000):
    if(i%5 == 0):
        volume += 2
        sp.volume(volume)
    if(volume == 100):
        break
