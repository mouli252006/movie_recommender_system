import streamlit as st
import pickle
import pandas as pd
import requests


# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=4af3d0ea164fa66a484bf7d44d833522&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=4af3d0ea164fa66a484bf7d44d833522&language=en-US".format(movie_id)
#     try:
#         data = requests.get(url).json()
#         poster_path = data.get('poster_path')
#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500//" + poster_path
#         return None  # or placeholder URL
#     except:
#         return None

# 4af3d0ea164fa66a484bf7d44d833522



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

# import requests

API_KEY ='4af3d0ea164fa66a484bf7d44d833522' 

# @st.cache_data
def fetch_poster(movie_id):
    placeholder = "https://via.placeholder.com/500x750?text=No+Image"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }
    headers = {
        # "User-Agent": "Mozilla/5.0"
        "accept": "application/json",
        "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0YWYzZDBlYTE2NGZhNjZhNDg0YmY3ZDQ0ZDgzMzUyMiIsIm5iZiI6MTc2NjY2Nzg3Ny43MTUwMDAyLCJzdWIiOiI2OTRkMzY2NTEzNzQyYWU1NjY4MTE4MjMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.AXjBbeZ2T-687_UKG2xct8bP6Y2RwT6-pBLgk285BE0"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        # if response.status_code != 200:
        #     return None

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/original" + poster_path
        # else:
        #     return placeholder

    except requests.exceptions.RequestException:
        return placeholder
    

# import time

# def recommend(movie):
#     # Get the index of the selected movie
#     movie_index = movies[movies['title'] == movie].index[0]
    
#     # Get similarity scores for this movie
#     distances = similarity[movie_index]
    
#     # Get top 5 similar movies (skip the first one because it's the same movie)
#     movies_list = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )[1:6]

#     recommended_movies = []
#     recommended_movies_posters = []

#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
        
#         # Fetch poster using the fixed function
#         poster = fetch_poster(movie_id)
#         recommended_movies_posters.append(poster)
        
#         # Small delay to prevent TMDB from blocking
#         time.sleep(0.7)

#     return recommended_movies, recommended_movies_posters



movies = pickle.load(open('movies.pkl','rb'))
movies_list=movies['title'].values


similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
selected_movie_name  = st.selectbox(
    "select your movie", movies_list
)

# movies_list=pd.DataFrame(movies_list)

if st.button('Recommend'):
    # st.write(type(movies_list))
    names , posters = recommend(selected_movie_name)

    col1 , col2, col3 , col4 , col5 =st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    
    