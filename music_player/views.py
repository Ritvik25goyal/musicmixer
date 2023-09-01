import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import requests
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse


def login(request):
    auth_url  = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

def redirect_page(request):
    request.session.flush()
    code = request.GET['code']
    token_info = create_spotify_oauth().get_access_token(code)
    request.session['TOKEN_INFO'] = token_info
    return redirect('get_user_profile')

def get_user_profile(request):
    try:
        token_info = get_token(request=request)
        auth =token_info['access_token']
        headers = {'Authorization': f'Bearer {auth}'}
    except:
        return HttpResponse('User not logged in')

    #offset possible
    artist_request = requests.get("https://api.spotify.com/v1/me/top/artists", headers=headers)
    return JsonResponse(artist_request.json())
    artists = r.json()['items']
    artist_ids = []
    for i in range(0,5):
        try:
            artist_ids.append(artists[i]['id'])
        except:
            break
    artist_ids = "%2C".join(artist_ids)

    r = requests.get(f"https://api.spotify.com/v1/recommendations?seed_artists={artist_ids}")
    tracks = r.json()['tracks']
    return JsonResponse(tracks)

    r_artists_all_time = requests.get("https://api.spotify.com/v1/me/top/artists?time_range=long_term&offset=10", headers=headers)
    return HttpResponse(type(r_artists_all_time))
    r_tracks_all_time = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=long_term&offset=50", headers=headers).json()

    r_artists_recent = requests.get("https://api.spotify.com/v1/me/top/artists?time_range=short_term&offset=10", headers=headers).json()
    r_tracks_recent = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=short_term&offset=50", headers=headers).json()

    #offset not possible
    r_tracks_recently_listened = (requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50", headers=headers)).json()

    ####Suggestions based on recent listening####

    features_of_track_avg = {"acousticness": 0 , "danceability" : 0, "energy":0, "liveness":0, "loudness":0}

    for feature in features_of_track_avg.keys():
        for track in r_tracks_recently_listened:
            track_id = track['id']
            track_features = requests.get("https://api.spotify.com/v1/audio-features?ids={track_id}").json()['audio_features'][0]
            features_of_track_avg[feature] += track_features[feature]
        features_of_track_avg[feature] = features_of_track_avg[feature]/50
    
    track_ids = []
    artist_ids = []
    for i in range(3):
        track_ids.append(r_tracks_recent[i]['id'])
    for i in range(2):
        artist_ids.append(r_artists_recent[i]['id'])
    artist_ids = "%2C".join(artist_ids)
    track_ids = "%2C".join(track_ids)

    r_sug_recent_listening = requests.get(
        f'''https://api.spotify.com/v1/recommendations?seed_artists={artist_ids}&seed_tracks={track_ids}
        &target_acousticness={features_of_track_avg['acousticness']}
        &target_danceability={features_of_track_avg['danceability']}
        &target_liveness={features_of_track_avg['liveness']}
        &target_energy={features_of_track_avg['energy']}
        &target_loudness={features_of_track_avg['loudness']}''', headers=headers).json()['items']


    ####Suggestions based on genre####

    favorite_genres = {}

    for artist in r_artists_all_time:
        artist_genres = artist['genres']
        for genre in artist_genres:
            if genre in favorite_genres.keys():
                favorite_genres[genre] += 1
            else:
                favorite_genres[genre] = 1
    
    for track in r_tracks_all_time:
        artists = track['artists']
        for artist in artists:
            artist_genres = artist['genres']
            for genre in artist_genres:
                if genre in favorite_genres.keys():
                    favorite_genres[genre] += 1
                else:
                    favorite_genres[genre] = 1
    
    top_3_genres = sorted(favorite_genres, key=favorite_genres.get, reverse=True)[:3]
    genre_recommendations = {}

    for genre in top_3_genres:
        genre_recommendations[genre] = requests.get(f"https://api.spotify.com/v1/recommendations?seed_genre={genre}", headers=headers)

   
def get_token(request):
    token_info  = request.session.get('TOKEN_INFO')
    if not token_info:
        return HttpResponse("No token in cookies")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        token_info = create_spotify_oauth().refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="28335f718466458e9b3157d14607750b",
        client_secret= "e1152a738d7d40d59d9a8ce7b9850698",
        redirect_uri= 'http://127.0.0.1:8000/redirect/',
        scope='user-library-read user-top-read',)
