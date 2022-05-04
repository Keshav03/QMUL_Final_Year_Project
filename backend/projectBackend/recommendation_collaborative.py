from xml.dom import IndexSizeErr
import pandas as pd
import os
import csv

import numpy as np

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

np.seterr(invalid='ignore')


gamescsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/vg.csv'
games = pd.read_csv(gamescsvFilePath, usecols=['gameid','name','year','genre','publisher','image','description'],dtype={'gameid':'int32','name': 'str', 'year': 'int32', 'genre':'str','publisher':'str','image':'str','description':'str'})

ratingcsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/gameUserRatings.csv'
ratings = pd.read_csv(ratingcsvFilePath, usecols=['userid','gameid','rating'],dtype={'userid':'int32','gameid': 'int32','rating':'float32'})

ganesMetric  = ratings.groupby('gameid').agg({'rating':[np.size,np.mean]})


# game_user_ratings = ratings.pivot(index='gameid',columns='userid',values='rating')
# game_user_ratings.to_csv(os.path.dirname(os.path.abspath(__file__)) + '/datasets/pivot.csv',index=True)
game_user_ratings = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/datasets/pivot.csv',index_col=0)

# game_user_ratings = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/datasets/small_movie_ratings.csv',index_col=0)

print(game_user_ratings)

def find_correlation_between_two_users(ratings_df: pd.DataFrame, user1: str, user2: str):
    """Find correlation between two users based on their rated movies using Pearson correlation"""
    rated_movies_by_both = ratings_df[[user1, user2]].dropna(axis=0).values
    user1_ratings = rated_movies_by_both[:, 0]
    user2_ratings = rated_movies_by_both[:, 1]
    return np.corrcoef(user1_ratings, user2_ratings)[0, 1]

users = list(game_user_ratings.columns)
print(users)
movies = list(game_user_ratings.index)
print(movies)
similarity_matrix = np.array([[find_correlation_between_two_users(game_user_ratings, user1, user2) for user1 in users] for user2 in users])
similarity_df = pd.DataFrame(similarity_matrix, columns=users, index=users)
similarity_df


def get_rated_user_for_a_game(ratings, gameid):
    return ratings.loc[gameid, :].dropna().index.values

def get_top_neighbors(similarity_df: pd.DataFrame, user: str, rated_users: str, n_neighbors: int):
    return similarity_df[user][rated_users].nlargest(n_neighbors).to_dict()

def subtract_bias(rating: float, mean_rating: float):
    return rating - mean_rating


def get_neighbor_rating_without_bias_per_movie(
    ratings_df: pd.DataFrame, user: str, movie: str
):
    """Substract the rating of a user from the mean rating of that user to eliminate bias"""
    mean_rating = ratings_df[user].mean()
    rating = ratings_df.loc[movie, user]
    return subtract_bias(rating, mean_rating)
    
def get_ratings_of_neighbors(ratings_df: pd.DataFrame, neighbors: list, movie: str):
    """Get the ratings of all neighbors after adjusting for biases"""
    return [
        get_neighbor_rating_without_bias_per_movie(ratings_df, neighbor, movie)
        for neighbor in neighbors
    ]
    

def get_weighted_average_rating_of_neighbors(ratings: list, neighbor_distance: list):
    weighted_sum = np.array(ratings).dot(np.array(neighbor_distance))
    abs_neigbor_distance = np.abs(neighbor_distance)
    return weighted_sum / np.sum(abs_neigbor_distance)

def ger_user_rating(ratings_df: pd.DataFrame, user: str, avg_neighbor_rating: float):
    user_avg_rating = ratings_df[user].mean()
    return round(user_avg_rating + avg_neighbor_rating, 2)





def predict_rating(df: pd.DataFrame,similarity_df: pd.DataFrame,user: str,movie: str,n_neighbors: int =2):
    """Predict the rating of a user for a movie based on the ratings of neighbors"""
    ratings_df = df.copy()
    rated_users = get_rated_user_for_a_game(ratings_df, movie)
    top_neighbors_distance = get_top_neighbors(similarity_df, user, rated_users, n_neighbors)
    neighbors, distance = top_neighbors_distance.keys(), top_neighbors_distance.values()
    print(f"Top {n_neighbors} neighbors of user {user}, {movie}: {list(neighbors)}")
    ratings = get_ratings_of_neighbors(ratings_df, neighbors, movie)
    avg_neighbor_rating = get_weighted_average_rating_of_neighbors(ratings, list(distance))
    return ger_user_rating(ratings_df, user, avg_neighbor_rating)



for i  in range (5):
    full_ratings = game_user_ratings.copy()
    for user, games in full_ratings.iteritems():
        for gameid in games.keys():
            if np.isnan(full_ratings.loc[gameid, user]):
                full_ratings.loc[gameid, user] = predict_rating(game_user_ratings, similarity_df, user, gameid)



print(full_ratings)

# usersRatingScores = []
# userid= 1

# #current user objects
# user ={"name":userid}

# with open(gamescsvFilePath) as csvf:
#                 gamecsvReader = csv.DictReader(csvf)
#                 temp = 0
#                 for rows1 in gamecsvReader:

#                     with open(ratingcsvFilePath) as csvf:
#                         ratingcsvReader = csv.DictReader(csvf)
#                         for rows2 in ratingcsvReader:
#                             if(userid == int(rows2["userid"])):
#                                 if(int(rows2["gameid"])==int(rows1["gameid"])):
#                                     temp = int(rows2["rating"])
#                     user[rows1["gameid"]] = temp 
#                     temp = 0


# #list of other users
# userList= []

# model = NearestNeighbors(metric='cosine',algorithm='brute' , n_neighbors= 5)
# # model.fit(matrix)