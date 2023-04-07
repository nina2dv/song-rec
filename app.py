import streamlit as st
from multipage import MultiPage
from apps import artist, song, song2

app = MultiPage()
st.set_page_config(
    page_title="Music Recommendations",
    page_icon="🎵",
    layout="wide")

st.markdown("""
# Music Recommendation

""")

# Add all your application here
app.add_app("Artist", artist.app)
app.add_app("Track", song.app)
app.add_app("Tracks", song2.app)

st.markdown("""---""")
app.run()
