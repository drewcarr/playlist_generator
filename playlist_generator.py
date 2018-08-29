import heapq
import random

import numpy as np
import xml.etree.ElementTree as ET
import urllib.request, json

tracks = []
playlist = []
min_year = 0
max_year = 0
min_skips = 0
max_skips = 0
min_plays = 0
max_plays = 0
genres = []
weights = []
biases = []

def get_tracks():
    library = ET.parse('Music.xml')
    root = library.getroot().find('dict').find('dict')

    ## Gets each song
    for child in root.findall('dict'):
        ## Gets info on each song
        dict = {'Track ID': None, 'Genre': None, 'Year': None, 'Play Count': 0, 'Skip Count': 0}

        for i in range (0, len(child)):
            if (child[i].text == 'Track ID'):
                dict['Track ID'] = child[i+1].text
            if (child[i].text == 'Genre'):
                dict['Genre'] = child[i+1].text
            if (child[i].text == 'Year'):
                dict['Year'] = child[i+1].text
            if (child[i].text == 'Play Count'):
                dict['Play Count'] = child[i+1].text
            if (child[i].text == 'Skip Count'):
                dict['Skip Count'] = child[i+1].text
        if (dict['Year']):
            tracks.append(dict)

    print('Loaded {} tracks from Music.xml' .format(len(tracks)))

def get_playlist(playlist_name):
    library = ET.parse('Library.xml')
    root = library.getroot().find('dict').find('array')

    for child in root:
        if (child.find('string').text == playlist_name):
            playlist_tracks = child.find('array')
            continue

    for track in playlist_tracks.findall('dict'):
        heapq.heappush(playlist, track.find('integer').text)

    print('Loaded {} tracks from playlist {} using Library.xml' .format(len(playlist), playlist_name))

def get_mins_and_maxs ():
    global max_year
    global min_year
    global max_skips
    global min_skips
    global max_plays
    global min_skips

    min_year = int(tracks[0]['Year'])
    min_skips = int(tracks[0]['Skip Count'])
    min_plays = int(tracks[0]['Play Count'])

    print (len(tracks))

    for track in tracks:
        if (int(track['Year']) < min_year):
            min_year = int(track['Year'])
        if (int(track['Year']) > max_year):
            max_year = int(track['Year'])

        if (int(track['Play Count']) < min_plays):
            min_plays = int(track['Play Count'])
        if (int(track['Play Count']) > max_plays):
            max_plays = int(track['Play Count'])

        if (int(track['Skip Count']) < min_skips):
            min_skips = int(track['Skip Count'])
        if (int(track['Skip Count']) > max_skips):
            max_skips = int(track['Skip Count'])

def get_genres ():
    global genres
    with urllib.request.urlopen("http://itunes.apple.com/WebObjects/MZStoreServices.woa/ws/genres?id=34") as url:
        data = json.loads(url.read().decode())
        genres_dict = data['34']['subgenres']

        string_keys = genres_dict.keys()
        for key in string_keys:
            genres.append(genres_dict[str(key)]['name'])
            if ('subgenres' in genres_dict[str(key)].keys()):
                for k in genres_dict[str(key)]['subgenres'].keys():
                    genres.append(genres_dict[str(key)]['subgenres'][str(k)]['name'])

def get_input_vector (track):
    global min_plays, max_plays, min_skips, max_skips, min_year, max_year, genres
    year = (int(track['Year']) - min_year) / (max_year - min_year)
    plays = (int(track['Play Count']) - min_plays) / (max_plays - min_plays)
    skips = (int(track['Skip Count']) - min_skips) / (max_skips - min_skips)
    if (track['Genre'] in genres):
        genre = genres.index(track['Genre']) / len(genres)
    else:
        print ('Could not find genre: ', track['Genre'])
        ## Fixing Hip-Hop/Rap != Hip Hop/Rap
        genre = genres.index('Hip-Hop/Rap') / len(genres)


    return [year, plays, skips, genre]

def test_inputs ():
    for track in tracks:
        inputs = get_input_vector(track)
        for input in inputs:
            if (input > 1):
                print ('ERROR WITH INPUT ', track['Track ID'])

def generate_weights_and_biases (sizes):
    """ Sizes should be a list representing number of neurons in each layer
        Ex: [4,3,1] """
    biases = [np.random.randn(y, 1) for y in sizes[1:]]
    weights = [np.random.randn(y, x)
                    for x, y in zip(sizes[:-1], sizes[1:])]

def sigmoid (z):
    return 1.0/(1.0 + np.exmp(-z))

def feedforward (a):
    for b, w in zip(biases, weights):
        a = sigmoid(np.dot(w, a) + b)
    return a

get_tracks()
get_playlist('Lake')
get_mins_and_maxs()
get_genres()
test_inputs()
generate_weights_and_biases([4,3,1])
