import streamlit as st
import pickle
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="🎬 MovieVerse AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

movies = pickle.load(open("artifacts/movies.pkl", "rb"))
similarity = pickle.load(open("artifacts/similarity.pkl", "rb"))

# ---------------------------------------------------
# RECOMMENDATION FUNCTION
# ---------------------------------------------------

def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies
# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

.stApp{
    background:linear-gradient(135deg,#0f172a,#111827,#000000);
    color:white;
}

/* Hide Streamlit Elements */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #333;
}

/* Main Title */

.title{
    text-align:center;
    font-size:58px;
    font-weight:800;
    color:#ff4b4b;
    margin-top:20px;
    margin-bottom:0px;
}

.subtitle{
    text-align:center;
    font-size:20px;
    color:#d1d5db;
    margin-bottom:40px;
}

/* Search Card */

.card{
    background:#1f2937;
    padding:25px;
    border-radius:20px;
    border:1px solid #374151;
    box-shadow:0px 8px 25px rgba(0,0,0,.35);
    margin-top:20px;
    margin-bottom:25px;
}

/* Recommend Button */

.stButton>button{
    width:100%;
    background:#ff4b4b;
    color:white;
    border:none;
    border-radius:10px;
    padding:14px;
    font-size:18px;
    font-weight:bold;
    transition:.3s;
}

.stButton>button:hover{
    background:#ff2d2d;
    transform:scale(1.02);
}

/* Recommendation Card */

.movie-card{
    background:#1f2937;
    border:1px solid #374151;
    border-radius:18px;
    padding:20px;
    text-align:center;
    transition:0.3s;
    box-shadow:0px 8px 20px rgba(0,0,0,.35);
    min-height:180px;
}

.movie-card:hover{
    transform:translateY(-8px);
    border:1px solid #ff4b4b;
    box-shadow:0px 12px 30px rgba(255,75,75,.35);
}

.movie-icon{
    font-size:48px;
    margin-bottom:10px;
}

.movie-title{
    color:white;
    font-size:18px;
    font-weight:700;
    margin-bottom:10px;
}

.movie-tag{
    color:#ff4b4b;
    font-size:14px;
    font-weight:600;
}

/* Footer */

.footer{
    text-align:center;
    margin-top:80px;
    padding:20px;
    color:#9ca3af;
    border-top:1px solid #333;
    font-size:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🎬 MovieVerse AI")

st.sidebar.markdown("---")

st.sidebar.subheader("📖 About")

st.sidebar.write("""
MovieVerse AI recommends movies using
**Machine Learning** and
**Cosine Similarity**.
""")

st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Features")

st.sidebar.write("✅ Smart Recommendations")
st.sidebar.write("✅ Fast Search")
st.sidebar.write("✅ Premium Interface")
st.sidebar.write("✅ Built with Python & Streamlit")

st.sidebar.markdown("---")

st.sidebar.success("👨‍💻 Developed by Pranav Shinde")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
<div class="title">
🎬 MovieVerse AI
</div>

<div class="subtitle">
Discover Your Next Favorite Movie with Artificial Intelligence
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SEARCH SECTION
# ---------------------------------------------------

st.markdown('<div class="card">', unsafe_allow_html=True)

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "🔍 Search Movie",
    movie_list
)

recommend_button = st.button("🎥 Recommend")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# RECOMMENDATION SECTION
# ---------------------------------------------------

if recommend_button:

    with st.spinner("🎬 Finding the perfect recommendations..."):
        recommendations = recommend(selected_movie)

    st.divider()

    st.markdown(
        f"""
        <h2 style='text-align:center; color:#ff4b4b;'>
        🎯 Because you liked <b>{selected_movie}</b>
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <p style='text-align:center; font-size:18px; color:#d1d5db;'>
        We found <b>{len(recommendations)}</b> similar movies for you.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    cols = st.columns(5)

    for i, movie in enumerate(recommendations):

        with cols[i]:

            with st.container(border=True):

                st.markdown(
                    "<h1 style='text-align:center;'>🎬</h1>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<h4 style='text-align:center;'>{movie}</h4>",
                    unsafe_allow_html=True
                )

                st.divider()

                st.caption("⭐ AI Recommendation")

                if st.button("View", key=f"btn_{i}"):
                    st.success(f"You selected **{movie}**")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(
"""
<div class="footer">

🎬 <b>MovieVerse AI</b>

<br><br>

Made with ❤️ by <b>Pranav Shinde</b>

<br><br>

© 2026 All Rights Reserved

</div>
""",
unsafe_allow_html=True
)