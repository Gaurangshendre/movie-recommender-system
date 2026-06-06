import streamlit as st
import pickle
import pandas as pd
import requests

# Set page config
st.set_page_config(
    page_title="CineSuggest - Premium Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom premium CSS styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

/* Main app formatting */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Outfit', sans-serif;
    background-color: #0b0c10;
}

/* Gradient Header */
.header-container {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem 1rem;
    background: linear-gradient(180deg, rgba(255, 75, 75, 0.1) 0%, rgba(0,0,0,0) 100%);
    border-radius: 0 0 30px 30px;
    margin-bottom: 2rem;
}

.header-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(45deg, #ff4b4b, #ff8f00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.header-subtitle {
    font-size: 1.2rem;
    color: #8f94a6;
    font-weight: 300;
    max-width: 600px;
    margin: 0 auto;
}

/* Card Styling */
.movie-card {
    background: rgba(31, 31, 31, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 12px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

.movie-card:hover {
    transform: translateY(-8px);
    border-color: #ff4b4b;
    box-shadow: 0 12px 30px rgba(255, 75, 75, 0.25);
    background: rgba(31, 31, 31, 0.95);
}

.movie-card img {
    border-radius: 12px;
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
}

.movie-title {
    margin-top: 12px;
    font-size: 1.05rem;
    font-weight: 600;
    color: #ffffff;
    height: 48px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
    line-height: 1.3;
}

/* Form block customization */
div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 2rem;
    max-width: 700px;
    margin: 0 auto 2.5rem auto;
}

/* Button Customization */
div.stButton > button {
    background: linear-gradient(45deg, #ff4b4b, #ff8f00);
    color: white !important;
    font-size: 1.1rem;
    font-weight: 600;
    padding: 0.6rem 2.5rem;
    border-radius: 30px;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    width: 100%;
    margin-top: 10px;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(255, 75, 75, 0.5);
}

div.stButton > button:active {
    transform: translateY(0);
}
</style>
""", unsafe_allow_html=True)

# Load data with caching to prevent slow re-runs
@st.cache_data
def load_data():
    try:
        with open('movies_dict.pkl', 'rb') as f:
            movies_dict = pickle.load(f)
        movies_df = pd.DataFrame(movies_dict)
        
        with open('similarity.pkl', 'rb') as f:
            similarity_matrix = pickle.load(f)
            
        return movies_df, similarity_matrix
    except Exception as e:
        st.error(f"Error loading files: {str(e)}")
        return None, None

movies, similarity = load_data()

# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
    # Fallback high quality cinema placeholder image
    return "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=500&auto=format&fit=crop"

# Recommendation logic
def recommend(movie_title):
    try:
        movie_idx = movies[movies['title'] == movie_title].index[0]
        distances = similarity[movie_idx]
        
        # Get top 5 most similar movies (excluding itself)
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        rec_names = []
        rec_posters = []
        for i in movies_list:
            m_id = movies.iloc[i[0]].movie_id
            rec_names.append(movies.iloc[i[0]].title)
            rec_posters.append(fetch_poster(m_id))
            
        return rec_names, rec_posters
    except Exception as e:
        st.error(f"Recommendation failed: {str(e)}")
        return [], []

# App Interface
st.markdown("""
<div class="header-container">
    <div class="header-title">🎬 CineSuggest</div>
    <div class="header-subtitle">Find your next cinematic masterpiece with our AI-powered movie recommendation engine.</div>
</div>
""", unsafe_allow_html=True)

if movies is not None and similarity is not None:
    # Centered container for movie selection
    col_l, col_c, col_r = st.columns([1, 2, 1])
    
    with col_c:
        selected_movie = st.selectbox(
            "Which movie did you enjoy?",
            movies['title'].values,
            index=0,
            help="Type or select a movie to get recommendations"
        )
        
        recommend_button = st.button("Generate Recommendations ✨")
        
    if recommend_button:
        with st.spinner("Analyzing ratings and similarity matrices..."):
            names, posters = recommend(selected_movie)
            
        if names and posters:
            st.write("---")
            st.markdown(f"<h3 style='text-align: center; color: #ff8f00; margin-bottom: 2rem;'>Because you liked <b>{selected_movie}</b>:</h3>", unsafe_allow_html=True)
            
            # Display recommendations in a responsive 5-column layout
            cols = st.columns(5)
            for idx in range(5):
                if idx < len(names):
                    with cols[idx]:
                        card_html = f"""
                        <div class="movie-card">
                            <img src="{posters[idx]}" alt="{names[idx]}">
                            <div class="movie-title">{names[idx]}</div>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
else:
    st.warning("Please ensure 'movies_dict.pkl' and 'similarity.pkl' are placed in the root directory of this project.")