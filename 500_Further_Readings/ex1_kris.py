"""
The program receives client_id, client_secret and playlist_id and creates a circular diagram
representing the statistics of the music you are listening to.

"""

import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import math

client_id = '6386b9851ba1422d986d0679664b823e'  # insert your client id
client_secret = '4082e30c07924dd68dc284dec52c3e4a'  # insert your client secret id here

auth_manager = SpotifyClientCredentials(client_id, client_secret)
sptfy = spotipy.Spotify(client_credentials_manager=auth_manager)

playlist_id = 'spotify:playlist:37i9dQZEVXcVCRUrQ42Ej9'  # insert your playlist id
results = sptfy.playlist(playlist_id)

# create a list of song ids
song_ids = []

for item in results['tracks']['items']:
    track = item['track']['id']
    song_ids.append(track)

song_data = {'id': [], 'album': [], 'name': [],
             'artist': [], 'popularity': []}

for song_id in song_ids:
    meta = sptfy.track(song_id)  # get song's meta data
    song_data['id'].append(song_id)  # song id

    album = meta['album']['name']  # album name
    song_data['album'] += [album]

    song = meta['name']  # song name
    song_data['name'] += [song]

    separator = ', '
    artist = separator.join([singer_name['name'] for singer_name in meta['artists']])  # artists name
    song_data['artist'] += [artist]

    # song popularity
    popularity = meta['popularity']
    song_data['popularity'].append(popularity)

song_meta_df = pd.DataFrame.from_dict(song_data)

# check the song feature
features = sptfy.audio_features(song_data['id'])
# change dictionary to dataframe
features_df = pd.DataFrame.from_dict(features)

# convert milliseconds to mins
# duration_ms: The duration of the track in milliseconds.
# 1 minute = 60 seconds = 60 × 1000 milliseconds = 60,000 ms
features_df['duration_ms'] = features_df['duration_ms'] / 60000
final_df = song_meta_df.merge(features_df)

#print(final_df)

music_feature = features_df[['danceability', 'energy', 'loudness', 'speechiness', 'valence',
                             'tempo', 'duration_ms', 'acousticness', 'liveness', 'instrumentalness']]

# Normalization - transfrom values in the range 0-1
min_max_scaler = MinMaxScaler()
music_feature.loc[:] = min_max_scaler.fit_transform(music_feature.loc[:])

# plot size
fig = plt.figure(figsize=(8, 8))

# convert column names into a list
categories = list(music_feature.columns)
# number of categories
N = len(categories)

# create a list with the average of all features
value = list(music_feature.mean())

# repeat first value to close the circle
# the plot is a circle, so we need to "complete the loop"
# and append the start value to the end.
value += value[:1]
# calculate angle for each category
angles = [n / float(N) * 2 * math.pi for n in range(N)]
angles += angles[:1]

# plot
plt.polar(angles, value)
plt.fill(angles, value, alpha=0.3)

# plt.title('Discovery Weekly Songs Audio Features', size=35)

plt.xticks(angles[:-1], categories, size=15)
plt.yticks(color='grey', size=15)
plt.show()
