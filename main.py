import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch poster from TMDb API
def fetch_poster(movie_id):
    if movie_id is None or pd.isna(movie_id):  # safeguard
        return "https://via.placeholder.com/500x750?text=No+Poster"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=40000c123ff53dc64edb459afa75bdc5&language=en-US"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie_id={movie_id}:", e)
        return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id if "movie_id" in movies.columns else None
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movies_list = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit UI
st.title("🎬 Movie Recommendation System")

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])
