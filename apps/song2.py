import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit.components.v1 as components

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=st.secrets['id'],
                                                           client_secret=st.secrets['secret']))


def get_track(name):
    results = sp.search(q=name, type='track', limit=50)
    items = results['tracks']['items']
    # st.write(items)
    ids = [i["id"] for i in items]
    if len(items) > 0:
        return ids
    else:
        return None


def show_recommendations_for_track(music):
    results = sp.recommendations(seed_tracks=music[0:4], limit=50)
    track_list = []
    for track in results['tracks']:
        temp = """<iframe src="https://open.spotify.com/embed/track/{}" width="260" height="330" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(track["id"])
        track_list.append({"name": track['name'], "artists": track['artists'][0]['name'], "embed": temp})
    return track_list


def app():
    st.markdown("""---""")

    form = st.form(key='my_form')
    search = form.text_input(label='Track : ')
    submit_button = form.form_submit_button(label='Enter')
    if submit_button:
        track = get_track(search)
        wcol = 4
        cols = st.columns(4)
        temp_count = 0

        if track:
            for count, value in enumerate(track):
                if temp_count >= len(track):
                    temp_count = 0
                else:
                    temp_count += 1
                col = cols[temp_count % wcol]
                with col:
                    temp = """<iframe src="https://open.spotify.com/embed/track/{}" width="260" height="330" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(
                        value)
                    components.html(temp, height=330)
        else:
            st.warning("Can't find that track")
        st.subheader("Recommendations")

        if track:
            name = show_recommendations_for_track(track)

            for count, value in enumerate(name):
                if temp_count >= len(name):
                    temp_count = 0
                else:
                    temp_count += 1
                col = cols[temp_count % wcol]
                with col:
                    st.write(f"{value['name']} - {value['artists']}")
                    components.html(value['embed'], height=330)
        else:
            st.warning("Can't find that track")