import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

dataset=pd.read_excel(r'./fmovies.xlsx')

dataset=dataset.drop_duplicates()
dataset=dataset.dropna(subset=['title'])
# print(dataset.head())
def Recommend( features):
    input_movie = input(' Enter any movie name : ')

    Allmovies = dataset['title'].tolist()
# final movie is the variable that will be given for recommendation
    if input_movie in Allmovies:
        finalmovie=input_movie
    else:
        # this is built in function that gives best 3 matches from the list
        firstsearch = difflib.get_close_matches(input_movie, Allmovies)
        # print(firstsearch)
        secondsearch = difflib.get_close_matches(input_movie, firstsearch)
        if len(secondsearch)==0:
            print(" There is no movie like ",input_movie," in dataset")
            return
        print(secondsearch)
        finalmovie = secondsearch[0]
        print(finalmovie)

    # finalmovie is the final name of movie that we will give to model for prediction
    for everyfeature in features:
        dataset[everyfeature] = dataset[everyfeature].fillna('')

    # this will get data from every feature and make a string that will contain data of all features
    modeldata = ''
    for everyfeature in features:
        modeldata = modeldata + ' ' + dataset[everyfeature]

    # print(modeldata[0])

    # fit function will train the model and transform will convert training data into vefctors
    AImodel = TfidfVectorizer()
    AImodel.fit(modeldata)
    AImodelvectors = AImodel.transform(modeldata)
    # print(AImodelvectors)

    # cosine will calculate theeta or distance between every vector, dataset will be matrix that will have distances of
    # all vectors or movies
    distanceset = cosine_similarity(AImodelvectors)

    # this is bulit in fucnction for getting index of our input or final movie
    finalmovie_index = dataset[dataset.title == finalmovie]['index'].values[0]

    # ex will contain similarity with every movie of input movie
    ex = distanceset[finalmovie_index]

    # slist will have tuples, each tuple have moviename on 0 index and distance on 1 index
    slist = []
    for i in range(len(Allmovies)):
        tp = (Allmovies[i], ex[i])
        slist.append(tp)

    c = slist.copy()
    title = []
    dist = []
    sorted = []
    for j in range(len(c)):
        title.append(c[j][0])
        dist.append(c[j][1])
    # print(max(dist))
    for i in range(len(c)):
        sorted.append((title.pop(dist.index(max(dist))), dist.pop(dist.index(max(dist)))))
    # print(sorted)
    print("Top 10 recommendations for ",finalmovie," are : ")
    for i in range(1, 11):
        print("Recommendation No :  ", i ,") ", sorted[i][0])

# Start of project
print('        WELCOME TO MOVIE RECOMMENDATION SYSTEM   \n\n')
print('Here you can get recommendations on basis of many categories\n')

# features is a list that contains the features on which recommendation will be given
while True:
    print('Press 1 for get recommendation on basis of Genres')
    print('Press 2 for get recommendation on basis of Actors')
    print('Press 3 for get recommendation on basis of Directors')
    print('Press 4 for get recommendation on basis of Rattings')
    print('Press 5 for get overall recommendation of movie :-')
    input_choice=input()

    if input_choice=="1":
        features=['genres']
        Recommend(features)

    elif input_choice=="2":
        features=['cast']
        Recommend(features)

    elif input_choice=="3":
        features=['director']
        Recommend(features)

    elif input_choice=="4":
        features=['vote_average']
        Recommend(features)

    elif input_choice=="5":

        features=['genres','cast','tagline','director']
        Recommend(features)

    else:
        print("Enter valid option\n")

