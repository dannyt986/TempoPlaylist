#!/usr/bin/python

import spotipy
import spotipy.util as util

username = 'swissdanny_67'
scope = 'playlist-modify-private'
client_id = 'de34433c465947d7af723d25cbbfc821'
client_secret ='08f65a7b32774eacb9bd2a8a0a1a5a8c'
redirect_uri = 'http://vps184910.vps.ovh.ca'
cache_path = '/var/www/html/tempoplaylist'

token = util.prompt_for_user_token(
        username,
        scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

def get_artist(name):
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def print_results(results):
        for xyz in results['tracks']:
                xyz_id = xyz['id']
                # print xyz_id
                xyz_feat = spotify.audio_features(tracks=[xyz_id])
                # print xyz_feat
                print xyz['name'], '-', xyz['artists'][0]['name']
                print xyz_feat[0]['tempo']

def parse_results(results):
    id_list = []
    parsed_list = []
    #track_data = []
    for track in results['tracks']:
         id_list.extend([track['id']])
    track_features = spotify.audio_features(tracks=id_list)
    index = 0
    for track in results['tracks']:
        parsed_list.insert(index, [index, track['id'], track['name'], track['artists'][0]['name'], track_features[index]['tempo'], track['external_urls']['spotify'] ] )
        index += 1
    for track in parsed_list:
            print track
    return id_list

def get_artist(name):
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        print items[0]['id']
        return items[0]['id']
    else:
        return None

if token:
        spotify = spotipy.Spotify(auth=token)
        tempo_input = 165 # raw_input("Target tempo[165]? ") or 165
        energy_input = None # raw_input("Target energy[0.8]? ") or None
        genre_input = None # raw_input("Genre[rock]? ") or 'rock'
        tracks_input = 25 #raw_input("Recommend[20]? ") or 20
        artist_input = raw_input("Artist? ") or 'The Strokes'
        print "Inputs: ", tempo_input, energy_input, genre_input, tracks_input, artist_input
        artist_id = get_artist(artist_input)

        results = spotify.recommendations(
                seed_artists = [artist_id] ,
                seed_genres = None, # [genre_input],
                seed_tracks = None,
                limit = tracks_input,
                country = 'CH',
                min_energy=energy_input,
                target_tempo=tempo_input)
                #min_tempo=160,
                #max_tempo=170)
        track_ids = parse_results(results)
        playlist_name = 'Running %s %d BPM' % (genre_input, tempo_input)
        existing_playlists = spotify.current_user_playlists(limit=50)
        for playlist in existing_playlists['items']:
            print(playlist['name'])
        if any(playlist_name in s for s in existing_playlists):
            already_exists = True
            # playlist_id = [id of playlist with name == name]
        else:
            playlist_id = spotify.user_playlist_create(username, playlist_name, public=False)
            already_exists = False
        # wait_here = raw_input("Enter to finish...")
        spotify.user_playlist_add_tracks(username, playlist_id['id'], track_ids)

else:
        print("Cant get token for", username)