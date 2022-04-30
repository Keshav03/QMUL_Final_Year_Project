import pandas as pd
import numpy as np
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def recommendationContentBased(request):

    if (request.method == "POST"):
        game = request.POST.get('name')
        print(game)
        gamescsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/vg.csv'
        games = pd.read_csv(gamescsvFilePath, usecols=['gameid','name','year','genre','publisher','image','description'],dtype={'gameid':'int32','name': 'str', 'year': 'int32', 'genre':'str','publisher':'str','image':'str','description':'str'})

        def convertToList(x):
            list1 = []
            if isinstance(x,int):
                x=str(x)
            x = x.split(" ")
            for i in x:
                list1.append(i)
            return list1  

        games['year'] = games['year'].apply(convertToList)
        games['genre'] = games['genre'].apply(convertToList)
        games['publisher'] = games['publisher'].apply(convertToList)
        games['description'] = games['description'].apply(lambda x:x.split())

        games['tags'] = games['description'] + games['genre'] + games['publisher']

        # games = games.drop(columns=['description','genre','publisher','year'])

        games['tags'] = games['tags'].apply(lambda x: " ".join(x))


        cv = CountVectorizer(max_features=1000,stop_words='english')
        vector = cv.fit_transform(games['tags']).toarray()
        similarity_score = cosine_similarity(vector)

        result = recommend(games,similarity_score,game)

        return JsonResponse({"top5":result})




def recommend(gameSet,similarityScore,game):
    try:
        index = gameSet[gameSet['name'] == game].index[0]
        distances = sorted(list(enumerate(similarityScore[index])),reverse=True,key = lambda x: x[1])
        result = []
        for i in distances[1:6]:
            json = {"name":gameSet.iloc[i[0]]["name"],"year":gameSet.iloc[i[0]]["year"],"genre":gameSet.iloc[i[0]]["genre"],"publisher":gameSet.iloc[i[0]]["publisher"],"image":gameSet.iloc[i[0]]["image"]}
            result.append(json)
    except:
        result = []
    
    return result

