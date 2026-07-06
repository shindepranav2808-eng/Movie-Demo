import pandas as pd
import numpy as np
import ast
import pickle
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from nltk.stem.porter import PorterStemmer

# Download NLTK data (only first time)
nltk.download('punkt')

ps = PorterStemmer()

# -----------------------------
# Load datasets
# -----------------------------

movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# -----------------------------
# Merge datasets
# -----------------------------

movies = movies.merge(credits, on="title")

# -----------------------------
# Select required columns
# -----------------------------

movies = movies[
    [
        'movie_id',
        'title',
        'overview',
        'genres',
        'keywords',
        'cast',
        'crew'
    ]
]

# -----------------------------
# Remove null values
# -----------------------------

movies.dropna(inplace=True)

# -----------------------------
# Helper Functions
# -----------------------------

def convert(text):
    L = []

    for i in ast.literal_eval(text):
        L.append(i['name'])

    return L


def convert3(text):
    L = []
    counter = 0

    for i in ast.literal_eval(text):

        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break

    return L


def fetch_director(text):

    L = []

    for i in ast.literal_eval(text):

        if i['job'] == 'Director':
            L.append(i['name'])

    return L
# -----------------------------
# Convert string columns to lists
# -----------------------------

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)

# -----------------------------
# Convert overview into list
# -----------------------------

movies['overview'] = movies['overview'].apply(lambda x: x.split())

# -----------------------------
# Remove spaces from names
# -----------------------------

movies['genres'] = movies['genres'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['keywords'] = movies['keywords'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['cast'] = movies['cast'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['crew'] = movies['crew'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

# -----------------------------
# Create tags column
# -----------------------------

movies['tags'] = (
    movies['overview']
    + movies['genres']
    + movies['keywords']
    + movies['cast']
    + movies['crew']
)

# Keep only required columns

new_df = movies[['movie_id', 'title', 'tags']]

# Convert list into string

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# Convert to lowercase

new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# -----------------------------
# Stemming Function
# -----------------------------

def stem(text):
    y = []

    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)

# Apply stemming

new_df['tags'] = new_df['tags'].apply(stem)

# -----------------------------
# Convert text into vectors
# -----------------------------

cv = CountVectorizer(
    max_features=5000,
    stop_words='english'
)

vectors = cv.fit_transform(new_df['tags']).toarray()

# -----------------------------
# Calculate Cosine Similarity
# -----------------------------

similarity = cosine_similarity(vectors)

print("Similarity matrix created successfully!")

# -----------------------------
# Create artifacts folder
# -----------------------------

os.makedirs("artifacts", exist_ok=True)

# -----------------------------
# Save the pickle files
# -----------------------------

with open("artifacts/movies.pkl", "wb") as f:
    pickle.dump(new_df, f)

with open("artifacts/similarity.pkl", "wb") as f:
    pickle.dump(similarity, f)

print("\n===================================")
print("Movie Recommender Model Created!")
print("===================================")
print("Files saved successfully:")
print("artifacts/movies.pkl")
print("artifacts/similarity.pkl")
print("===================================")