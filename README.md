# 🎬 CineSuggest - Movie Recommender System

A modern, AI-powered movie recommendation engine built with Streamlit that helps users discover their next favorite films based on movies they've already enjoyed.

## Features

- **Intelligent Recommendations**: Uses content-based filtering with similarity matrices to suggest movies similar to your selection
- **Beautiful UI**: Premium gradient design with smooth animations and responsive layout
- **Movie Posters**: Fetches real movie posters from TMDB API with fallback placeholders
- **Fast Search**: Cached data loading for instant performance
- **Simple Interface**: One-click movie selection and recommendation generation

## Technology Stack

- **Framework**: [Streamlit](https://streamlit.io/) - Web app framework
- **Data Processing**: Pandas, Pickle
- **API**: TMDB (The Movie Database) API for poster fetching
- **Styling**: Custom CSS with gradient effects and animations

## Prerequisites

Before running this project, ensure you have:
- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone or download** the repository to your local machine

2. **Install required dependencies**:
   ```bash
   pip install streamlit pandas requests
   ```

3. **Prepare required data files**:
   - `movies_dict.pkl` - Dictionary containing movie data (title, movie_id, etc.)
   - `similarity.pkl` - Similarity matrix for content-based recommendations
   
   Place both files in the root directory of the project

## Usage

1. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Select a movie** you enjoy from the dropdown menu

4. **Click "Generate Recommendations ✨"** to see 5 similar movies

## How It Works

### Recommendation Algorithm

The system uses **content-based filtering** with a precomputed similarity matrix:

1. When you select a movie, the app finds its index in the dataset
2. It retrieves similarity scores for all other movies using the similarity matrix
3. The top 5 most similar movies (excluding the input movie) are returned
4. Movie posters are fetched from TMDB API to enhance the visual experience

### Data Requirements

The project requires two pickle files:
- **movies_dict.pkl**: Contains movie metadata with at least:
  - `title`: Movie name
  - `movie_id`: TMDB movie ID for poster fetching
  
- **similarity.pkl**: Precomputed similarity matrix (numpy array or similar)

## API Configuration

The app uses the TMDB API to fetch movie posters. The current API key is included in the code, but you can replace it with your own by:

1. Visiting [TMDB API](https://www.themoviedb.org/settings/api)
2. Getting your API key
3. Updating the `api_key` variable in `app.py`

## Project Structure

```
movie-recommender-system/
├── app.py                  # Main Streamlit application
├── movies_dict.pkl         # Movie data (required)
├── similarity.pkl          # Similarity matrix (required)
└── README.md              # This file
```

## Troubleshooting

**Issue**: "Error loading files" message appears
- **Solution**: Ensure `movies_dict.pkl` and `similarity.pkl` are in the same directory as `app.py`

**Issue**: Movie posters not loading
- **Solution**: Check your internet connection. The app will display a fallback placeholder image if the API fails

**Issue**: Slow performance on first run
- **Solution**: This is normal. Streamlit caches the data after the first load for faster subsequent runs

## Features to Enhance

- Add filtering by genre, rating, or year
- Implement user ratings and feedback
- Add movie details (plot, cast, ratings)
- Implement collaborative filtering
- Add watchlist functionality
- Deploy to cloud platform (Heroku, AWS, etc.)

## License

This project is open source and available for personal and educational use.

## Author

Created as a movie recommendation system to demonstrate content-based filtering techniques.

---

**Enjoy discovering your next cinematic masterpiece! 🍿**
