import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from requests import Request, post
import requests
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

CLIENT_ID="28335f718466458e9b3157d14607750b"
CLIENT_SECRET= "e1152a738d7d40d59d9a8ce7b9850698"
REDIRECT_URL = 'http://127.0.0.1:8000/redirect/'

def home(request):
    return render(request, 'index.html')

def login(request):

    scope='user-library-read user-top-read user-read-recently-played user-read-email'

    url = Request('GET', "https://accounts.spotify.com/authorize", params = {
        'scope' : scope,
        'response_type' : 'code',
        'redirect_uri' : REDIRECT_URL,
        'client_id' : CLIENT_ID,
    }).prepare().url

    return redirect(url)

def redirect_page(request):
    request.session.flush()
    code = request.GET['code']
    
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : REDIRECT_URL,
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')

    request.session['access_token'] = access_token
    request.session['token_type'] = token_type
    request.session['refresh_token'] = refresh_token
    request.session['expires_in'] = expires_in

    return redirect('get_user_profile')

def get_user_profile(request):
    try:
        get_token(request=request)
        auth =request.session.get('access_token')
        headers = {'Authorization': f'Bearer {auth}'}

        context = {
            'access_token': request.session.get('access_token'),
            'auth': auth,
            'songs_json' : fetch_recent_recommendations(headers)
        }
        return JsonResponse(fetch_recent_recommendations(headers))
        return render(request, 'recommendations_recent.html', context)
    
    except:
        return HttpResponse('User not logged in')
    
def get_genre_recommendations(request):
        get_token(request=request)
        auth =request.session.get('access_token')
        headers = {'Authorization': f'Bearer {auth}'}

        context = {
                'access_token': request.session.get('access_token'),
                'auth': auth,
                'genre_recommendation' : fetch_genre_recommendations(headers)
        }

        return render(request, 'recommendations_genre.html', context)
        """     except:
            return HttpResponse('User not logged in') """
   
def get_token(request):
    access_token  = request.session.get('access_token')
    if not access_token:
        return HttpResponse("No token in cookies")
    now = int(time.time())
    is_expired = request.session.get('expires_in') - now < 60
    if (is_expired):
        return redirect('home')
    return None

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret= CLIENT_SECRET,
        redirect_uri= REDIRECT_URL,
        scope='user-library-read user-top-read user-read-recently-played user-read-email',)

def fetch_recent_recommendations(headers):
    r_artists_recent = requests.get("https://api.spotify.com/v1/me/top/artists?time_range=short_term&offset=10", headers=headers).json()
    r_tracks_recent = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=short_term&offset=50", headers=headers).json()
    r_tracks_recently_listened = (requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50", headers=headers)).json()

    return r_artists_recent

    try:
        features_of_track_avg = {"acousticness": 0 , "danceability" : 0, "energy":0, "liveness":0, "loudness":0}

        for feature in features_of_track_avg.keys():
            for track in r_tracks_recently_listened:
                track_id = track['id']
                track_features = requests.get(f"https://api.spotify.com/v1/audio-features?ids={track_id}").json()['audio_features'][0]
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
            &target_loudness={features_of_track_avg['loudness']}''', headers=headers).json()['tracks'][0:15]
        
        return (r_sug_recent_listening)
        
    except:
        return ({})
    
def fetch_genre_recommendations(headers):
    r_artists_all_time = requests.get("https://api.spotify.com/v1/me/top/artists?time_range=long_term&offset=10", headers=headers).json()['items']
    r_tracks_all_time = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=long_term&offset=50", headers=headers).json()['items']

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

    artists_in_fav_genres = {}

    for genre in top_3_genres:
        for artist in r_artists_all_time:
            artist_genres = artist['genres']
            if genre in artist_genres:
                artists_in_fav_genres[genre] = artist['id']

    genre_recommendations = {}

    for genre in top_3_genres:
        genre_recommendations[genre] = requests.get(f"https://api.spotify.com/v1/recommendations?seed_genres={genre}&seed_artists={artists_in_fav_genres[genre]}&limit=5", headers=headers).json()
    
    return (genre_recommendations)