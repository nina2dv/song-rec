import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit.components.v1 as components

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=st.secrets['id'],
                                                           client_secret=st.secrets['secret']))

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_recommendations_for_artist(artist):
    results = sp.recommendations(seed_artists=[artist['id']], limit=50)
    track_list = []
    for track in results['tracks']:
        temp = """<iframe src="https://open.spotify.com/embed/track/{}" width="260" height="320" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(track["id"])
        track_list.append({"name": track['name'], "artists": track['artists'][0]['name'], "embed": temp})
    return track_list

def app():
    st.markdown("""---""")

    form = st.form(key='my_form')
    search = form.text_input(label='Artist : ')
    submit_button = form.form_submit_button(label='Enter')

    if submit_button:

        artist = get_artist(search)

        st.subheader("Top Songs")
        wcol = 4
        cols = st.columns(4)
        temp_count = 0
        if artist:
            response = sp.artist_top_tracks("spotify:artist:" + artist['id'])['tracks']
            # st.write(response)
            for count, value in enumerate(response):
                if temp_count >= len(response):
                    temp_count = 0
                else:
                    temp_count += 1
                col = cols[temp_count % wcol]
                temp = """<iframe src="https://open.spotify.com/embed/track/{}" width="260" height="330" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(
                    value["id"])
                with col:
                    st.write(f"{value['name']}")

                    components.html(temp, height=330)
        else:
            st.warning("Can't find that artist")

        st.subheader("Recommendations")
        cols2 = st.columns(4)
        temp_count = 0
        if artist:
            name = show_recommendations_for_artist(artist)
            for count, value in enumerate(name):

                if temp_count >= len(name):
                    temp_count = 0
                else:
                    temp_count += 1
                col = cols2[temp_count % wcol]
                with col:
                    st.write(f"{value['name']} - {value['artists']}")
                    components.html(value['embed'], height=330)
        else:
            st.warning("Can't find that artist")