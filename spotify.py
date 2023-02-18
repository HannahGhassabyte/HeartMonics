#!/usr/bin/env python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID = "9c901f86b19f679869d93887a6bdb65cc3ac3736"
CLIENT_ID="d1dd10a583704bdea39276ffebbd0c32"
CLIENT_SECRET="28b55379b86e477bb1cedc57e2fbd856"
PL_ID = '5ngS6ldl3FmdTudnUJT0am' # playlist_id
HR = None # heartrate

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri="http://localhost:8080/",
                                                scope="user-read-playback-state,user-modify-playback-state"))

# Transfer playback to the Raspberry Pi if music is playing on a different device
#sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

# Song URI's 

##############################################################################
# This function 
def playSong():
    # playlist1 = []
    # results = sp.playlist_items(playlist_id='5ngS6ldl3FmdTudnUJT0am')
    # for i, track in enumerate(results['items']):
    #     try:
    #         playlist1.append(track['track']['uri'])
    #     except TypeError:
    #         None

    # print(playlist1)
    # sp.start_playback(device_id=DEVICE_ID, uris=[playlist1[0]])

    playlist1 = []
    results = sp.playlist_items(playlist_id='5ngS6ldl3FmdTudnUJT0am')
    for i, track in enumerate(results['items']):
        try:
            entry = {'name': track['track']['name'], 'uri': track['track']['uri']}
            playlist1.append(entry)
        except TypeError:
            None
    print(playlist1)
    sp.start_playback(device_id=DEVICE_ID, uris=[playlist1[0]])
#sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:45vW6Apg3QwawKzBi03rgD'])

playSong()  
#def selectPlaylist():