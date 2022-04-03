import streamlit as st 
import pandas as pd 
import pickle
import requests


similarity = pickle.load(open('contentmodel.pkl' , 'rb'))
new_dataframe = pd.DataFrame(pickle.load(open( 'moviesname_dict.pkl' ,'rb')))
movies=new_dataframe['title'].values

def fetch_poster(movie_id):
	response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=43abe5e3bad71d7313746d333e535a94'.format(movie_id))
	data = response.json()
	return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie):
    movie_index = new_dataframe[new_dataframe['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse = True , key=lambda x:x[1])[1:19] 
    recommended_movies=[]
    recommended_movies_posters =[]
    
    for i in movies_list :
         movie_id = new_dataframe.iloc[i[0]].movie_id
         recommended_movies.append(new_dataframe.iloc[i[0]].title)
         recommended_movies_posters.append(fetch_poster(movie_id))
        
    return recommended_movies ,recommended_movies_posters 

st.title('MOVIE RECOMMENDATION ENGINE !')
st.subheader('Using machine learning')
selectedmovie = st.selectbox(
     "Search for a movie you've liked in the past",
     movies)

st.write('You selected:', selectedmovie)
if st.button('Recommend'):
	names , posters  = recommend(selectedmovie)
	col1, col2 ,col3= st.columns(3)
	with col1:
		st.subheader(names[0])
		st.image(posters[0])
		
	with col2:
		st.subheader(names[1])
		st.image(posters[1])
		
	with col3:
		st.subheader(names[2])
		st.image(posters[2])
		
	with col1:
		st.subheader(names[3])
		st.image(posters[3])
	with col2:
	    st.subheader(names[4])
	    st.image(posters[4])

	with col3:
		st.subheader(names[5])
		st.image(posters[5])
	with col1:
	    st.subheader(names[6])
	    st.image(posters[6])

	with col2:
		st.subheader(names[7])
		st.image(posters[7])
	with col3:
	    st.subheader(names[8])
	    st.image(posters[8])

	with col1:
		st.subheader(names[9])
		st.image(posters[9])
	with col2:
	    st.subheader(names[10])
	    st.image(posters[10])

	with col3:
		st.subheader(names[11])
		st.image(posters[11])
	with col1:
	    st.subheader(names[12])
	    st.image(posters[12])

	with col2:
		st.subheader(names[13])
		st.image(posters[13])
	with col3:
	    st.subheader(names[14])
	    st.image(posters[14])
	with col1:
	    st.subheader(names[15])
	    st.image(posters[15])

	with col2:
		st.subheader(names[16])
		st.image(posters[16])
	with col3:
	    st.subheader(names[17])
	    st.image(posters[17])
