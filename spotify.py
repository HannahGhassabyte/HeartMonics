import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import random

DEVICE_ID="EDIT HERE"
CLIENT_ID="EDIT HERE"
CLIENT_SECRET="EDIT HERE"

ALARM = 0
SLOW = 1
MEDIUM = 2
FAST = 3


def spotify_init():
    # Spotify Authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                    client_secret=CLIENT_SECRET,
                                                    redirect_uri="http://localhost:8080",
                                                    scope="user-read-playback-state,user-modify-playback-state"))
    sp.shuffle(True, device_id=DEVICE_ID) # Shuffle on
    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

    # Pre-process saved playlists
    playlist_slow = []
    results = sp.playlist_items(playlist_id='0vvXsWCC9xrXsKd4FyS8kM')
    for i, track in enumerate(results['items']):
        try:
            entry = {'name': track['track']['name'], 'uri': track['track']['uri']}
            playlist_slow.append(entry)

        except TypeError:
            None
    
    playlist_med = []
    results = sp.playlist_items(playlist_id='2s6Y2vhOXPdbx9emkNab3k')
    for i, track in enumerate(results['items']):
        try:
            entry = {'name': track['track']['name'], 'uri': track['track']['uri']}
            playlist_med.append(entry)

        except TypeError:
            None

    playlist_fast = []
    results = sp.playlist_items(playlist_id='4Hi8QTO8mimKyPq4qrBjiZ')
    for i, track in enumerate(results['items']):
        try:
            entry = {'name': track['track']['name'], 'uri': track['track']['uri']}
            playlist_fast.append(entry)

        except TypeError:
            None

    return sp, playlist_slow, playlist_med, playlist_fast

def hr_logic(HR_VALUE, sp, prev_playlist_type, playlist_slow, playlist_med, playlist_fast):
    # Check HR and assign to a playlist catagory or alarm
    song_name = None
    next_playlist_type = prev_playlist_type
    playlist_uri_alarm = 'spotify:playlist:1Li4fkCNTZGzX5fXuAO9kU'
    playlist_uri_slow = 'spotify:playlist:0vvXsWCC9xrXsKd4FyS8kM'
    playlist_uri_med = 'spotify:playlist:2s6Y2vhOXPdbx9emkNab3k'
    playlist_uri_fast = 'spotify:playlist:4Hi8QTO8mimKyPq4qrBjiZ'

    if (HR_VALUE <= 50 or HR_VALUE > 150) and (prev_playlist_type != ALARM):
        sp.start_playback(device_id=DEVICE_ID, context_uri=playlist_uri_alarm, offset={"position":0})
        next_playlist_type = 0
        song_name = "Alarm"
    elif HR_VALUE > 50 and HR_VALUE <= 85 and (prev_playlist_type != SLOW):
        slow_song_position = random.randint(0,len(playlist_slow))
        fade_play(sp, playlist_uri_slow, slow_song_position)
        song_name = playlist_slow[slow_song_position]['name']
        next_playlist_type = 1
    elif HR_VALUE > 85 and HR_VALUE <=100 and (prev_playlist_type != MEDIUM):
        med_song_position = random.randint(0,len(playlist_med))
        fade_play(sp, playlist_uri_med, med_song_position)
        song_name = playlist_med[med_song_position]['name']
        next_playlist_type = 2
    elif HR_VALUE > 100 and HR_VALUE <= 150 and (prev_playlist_type != FAST):
        fast_song_position = random.randint(0,len(playlist_fast))
        fade_play(sp, playlist_uri_fast, fast_song_position)
        song_name = playlist_fast[fast_song_position]['name']
        next_playlist_type = 3

    return song_name, next_playlist_type

def fade_play(sp, uris_in, offset_in):
    # Regulates song transitions
    results = sp.currently_playing()
    is_playing = results['is_playing']
    if is_playing:
        volume = 100
        for i in range(0, 10000):
            if(i%5 == 0):
                volume -= 5
                sp.volume(volume)
            if(volume <= 0):
                break
        sp.start_playback(device_id=DEVICE_ID, context_uri=uris_in, offset={"position":offset_in})
        for i in range(0, 10000):
            if(i%5 == 0):
                volume += 5
                sp.volume(volume)
            if(volume >= 100):
                break
    else:
        sp.start_playback(device_id=DEVICE_ID, context_uri=uris_in, offset={"position":offset_in})

def toggle_play(sp):
    # check if already playing and toggle
    sp.volume(100)
    results = sp.currently_playing()
    is_playing = results['is_playing']
    if is_playing:
        sp.pause_playback(device_id=DEVICE_ID)
    else: 
        sp.start_playback(device_id=DEVICE_ID)

def skip(sp):
    sp.next_track(device_id=DEVICE_ID)

def previous(sp):
    sp.previous_track(device_id=DEVICE_ID)

def change_playback_device(sp):
    # Play music on next available connected device
    global DEVICE_ID
    id_1 = 'EDIT HERE'
    id_2 = 'EDIT HERE'
    
    if DEVICE_ID == id_1:
        DEVICE_ID = id_2
    else:
        DEVICE_ID = id_1
    sp.transfer_playback(device_id=DEVICE_ID, force_play=True)
