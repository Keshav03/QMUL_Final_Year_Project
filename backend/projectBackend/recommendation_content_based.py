import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import os

gamescsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/vg.csv'
userRatingscsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/gameUserRatings.csv'

games = pd.read_csv(gamescsvFilePath, usecols=['gameid','name','year','genre','publisher'],dtype={'gameid':'int32','name': 'str', 'year': 'str', 'genre':'str','publisher':'str'})
userRatings = pd.read_csv(userRatingscsvFilePath, usecols=['userid','gameid','rating'],dtype={'userid': 'int32', 'gameid':'int32','rating':'int32'})

print(games.head())
print(userRatings.head())


df = pd.merge(userRatings,games,on='gameid')
print(df.head())

game_rating = df.dropna(axis = 0, subset = ['name'])
game_ratingCount = (game_rating.
     groupby(by = ['name'])['rating'].
     count().
     reset_index().
     rename(columns = {'rating': 'RatingCount'})
     [['name', 'RatingCount']]
    )
print(game_ratingCount.head())

rating_with_totalRatingCount = game_rating.merge(game_ratingCount, left_on = 'name', right_on = 'name', how = 'left')
rating_with_totalRatingCount.head()

pd.set_option('display.float_format', lambda x: '%.3f' % x)
print(game_ratingCount['RatingCount'].describe())

popularity_threshold = 1
rating_popular_movie= rating_with_totalRatingCount.query('RatingCount >= @popularity_threshold')
print(rating_popular_movie.head())

print(rating_popular_movie.shape)

movie_features_df=rating_popular_movie.pivot_table(index='name',columns='userid',values='rating').fillna(0)


print("/////////////////////////////////////////////////")
print(movie_features_df.head())
print("////////////////////////////////////////////////")

from scipy.sparse import csr_matrix

movie_features_df_matrix = csr_matrix(movie_features_df.values)

from sklearn.neighbors import NearestNeighbors


model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(movie_features_df_matrix)


query_index = np.random.choice(movie_features_df.shape[0])
print(query_index)

distances, indices = model_knn.kneighbors(movie_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)

for i in range(0, len(distances.flatten())):
    if i == 0:
        print('Recommendations for {0}:\n'.format(movie_features_df.index[query_index]))
    else:
        print('{0}: {1}, with distance of {2}:'.format(i, movie_features_df.index[indices.flatten()[i]], distances.flatten()[i]))