import pandas as pd
import os

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

gamescsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/vg.csv'
games = pd.read_csv(gamescsvFilePath, usecols=['gameid','name','year','genre','publisher','image','description'],dtype={'gameid':'int32','name': 'str', 'year': 'int32', 'genre':'str','publisher':'str','image':'str','description':'str'})

ratingcsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/gameUserRatings.csv'
ratings = pd.read_csv(ratingcsvFilePath, usecols=['userid','gameid','rating'],dtype={'userid':'int32','gameid': 'int32','rating':'int32'})

game_user = ratings.pivot(index='gameid',columns='userid',values='rating').fillna(0)

matrix = csr_matrix(game_user.values)
print(matrix)

model = NearestNeighbors(metric='cosine',algorithm='brute' , n_neighbors= 5)
model.fit(matrix)



def recommend(name,matrix):
    index = process.extractOne(name,games['name'])[2]
    print(index)
    distance, indices =  model.kneighbors(matrix[index],n_neighbors=5)
    print(distance,indices)
    result = []
    for i in indices:
        json = {"name":games['name'][i],"year":games['year'][i],"genre":games['genre'][i],"publisher":games['publisher'][i],"image":games['image'][i]}
        result.append(json)
        print(json)
        print("///////////////")
    return




recommend("Grand Theft Auto V",matrix)
