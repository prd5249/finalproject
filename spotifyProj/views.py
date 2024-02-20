from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = 'a6435c78deec4ee184544256198dbd4e'
SPOTIPY_CLIENT_SECRET = '0ca777f3ca534444b8c35522281d9d8a'
# Create your views here.


def index(request):
    return render(request, "index.html")


def results(request):
    search_query = request.GET.get('searchType') + ':' + request.GET.get('search')
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                                                  client_secret=SPOTIPY_CLIENT_SECRET))
    topresults = spotify.search(search_query, limit=10, offset=0, type='album', market=None)
    shortresults = topresults['albums']['items']
    if not bool(shortresults):
        return render(request, "error.html")
    albumNameList = []
    artistNameList = []
    releaseDateList = []
    albumArt = []
    for result in shortresults:
        albumNameList.append(result['name'])
        currArtist = result['artists'][0]['name']
        if len(result['artists']) > 1:
            for i in range(1, len(result['artists'])):
                currArtist = currArtist + " & " + result['artists'][i]['name']

        artistNameList.append(currArtist)
        releaseDateList.append(result['release_date'])
        albumArt.append(result['images'][0]['url'])
        results = zip(albumNameList, artistNameList, releaseDateList, albumArt)
        context = { 'results' : results }
    return render(request, "results.html", context)
