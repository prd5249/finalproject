from django.shortcuts import render
# Importing spotipy, a simple interface for the Spotify API. This is used
# rather than raw calls to the Spotify API
import spotipy
# The Client Credentials allows me to 'seed' this configuration with two
# parameters required for using the spotify app, the Client ID & Secret
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError
# Needed to grab environment variables
import os

# Effectively the default view, this is used once with the index.html as the template
def index(request):
    return render(request, "index.html")

# The primary view where the user will see results
def results(request):
    # A user can select to search an album or an artist, so two parameters from the
    # query string are identified and used to create the Search query
    search_query = request.GET.get('searchType') + ':' + request.GET.get('search')
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                                                                  client_secret=os.environ["SPOTIPY_CLIENT_SECRET"]))

    # We've built the search command to use, and now we check with Spotify
    # I'm trying to limit the results so there is less to parse

    topresults = spotify.search(search_query, limit=10, offset=0, type='album', market=None)
    playlistResults = spotify.search(search_query, limit=10, offset=0, type='playlist', market=None)
    playlistLink = playlistResults['playlists']['items'][0]['external_urls']['spotify']
    # The JSON object returns a lot of information, but I'm only looking for the top 10 album results
    shortresults = topresults['albums']['items']
    # If there are NO RESULTS, I need to show an error page, so I redirect the user to a specific view for that
    if not bool(shortresults):
        return render(request, "error.html")

    # Initialize lists which will be populated based on the information received from Spotify
    # I'm trying to do as much work as possible here so the template results.html is much simpler
    albumNameList = []
    artistNameList = []
    releaseDateList = []
    albumArt = []
    # There are only 10 results, so looping through each of them
    for result in shortresults:
        albumNameList.append(result['name'])
        # We pull the 1st artist (or 0th, really) and store that, THEN check for additional artists
        # This is trying to pretify the names of the artists, otherwise the results don't look good here
        currArtist = result['artists'][0]['name']
        if len(result['artists']) > 1:
            for i in range(1, len(result['artists'])):
                currArtist = currArtist + " & " + result['artists'][i]['name']

        artistNameList.append(currArtist)
        releaseDateList.append(result['release_date'])
        albumArt.append(result['images'][0]['url'])

    # After everything for this result is identified, create a zip object for easily navigating on the html page
    searchResults = zip(albumNameList, artistNameList, releaseDateList, albumArt)
    context = { 'results' : searchResults, 'playlistLink' : playlistLink }
    # Create the webpage, passing in the results we've accumulated
    return render(request, "results.html", context)
