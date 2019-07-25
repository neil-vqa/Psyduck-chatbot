
import spotipy, random
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'c8c1c930c1714cff9e4f22b0ded3a4af'
client_secret = '042f3d1eb50e48fa8ba11c4706bd1563'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def show_recommendations_for_artist(artist):
    music_list = []
    results = sp.recommendations(seed_artists = [artist['id']])
    for track in results['tracks']:
        title = track['name']
        artist = track['artists'][0]['name']
        music_dat = {
                "title": title,
                "artist": artist
        }
        music_list.append(music_dat)
    final_list = random.sample(music_list, 8)
    return final_list


