#library installation
#pip install nltk
import nltk
import pandas as pd
import numpy as np
import ast 
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

#loading the data
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

#merging
movies = movies.merge(credits , on = 'title')

# features incude genre , id , keyword , title , overview , cast , crew 
movies=movies[['movie_id' , 'keywords' , 'title', 'overview' , 'genres' , 'cast' , 'crew' ]]
movies.dropna(inplace = True)

#feature conversions
def convert(obj):
        L =[]
        for i in ast.literal_eval(obj) :
                L.append(i['name'])
        return L

def convert3(obj):
    L= []
    counter = 0 
    for i in ast.literal_eval(obj):
        if counter != 5:
            L.append(i['name'])
            counter +=1
        else :
            break
    return L

def fetch_director(obj):
    L =[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director' :
            L.append(i['name'])
            break
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" " , "")for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" " , "")for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" " , "")for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" " , "")for i in x])
movies['tags'] = movies['overview'] + movies['keywords'] +movies['genres']+movies['cast'] +movies['crew']
new_dataframe = movies[['movie_id' , 'title' , 'tags']]
new_dataframe['tags'] =new_dataframe['tags'].apply(lambda x:" ".join(x))
new_dataframe['tags'] =new_dataframe['tags'].apply(lambda x:x.lower())

#feature  scaling
cv = CountVectorizer(max_features=5000 , stop_words='english')
vectors = cv.fit_transform(new_dataframe['tags']).toarray()
ps = PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
new_dataframe['tags'] = new_dataframe['tags'].apply(stem)
similarity =cosine_similarity(vectors)

#recomenddation function
def recommend(movie):
    movie_index = new_dataframe[new_dataframe['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse = True , key=lambda x:x[1])[1:11] 
    for i in movies_list :
        print(new_dataframe.iloc[i[0]].title)

print(recommend('Avatar'))