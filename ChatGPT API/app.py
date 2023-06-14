from flask import Flask, render_template, request, url_for, redirect
import openai
import spotipy
import joblib
import spotipy.util as util
import random
from moodtape_functions import authenticate_spotify, aggregate_top_artists, aggregate_top_tracks, select_tracks, create_playlist

client_id = 'fe950c4faf544e42af36cfa40473ccd3'
client_secret = 'c37d08196f3644a081b8dd97854e2be7'
redirect_uri = 'https://example.com/callback/'
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'

messages = [{'role': 'system',
             'content': 'Act as a chat bot that asks questions to understand the mood of the user and reply accordingly. if the user deviates and asks other questions not related to their mood, bring the user back to this. Keep the converstion only until the mood is clear or the user seems done chatting.'}]

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = "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"

global chat
chat = ''
global selected_tracks
selected_tracks = []
# Define the default route to return the index.html file


@app.route("/")
def start():
    return render_template("start.html")


@app.route("/chat")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests


@app.route("/api", methods=["POST"])
def api():
    global chat
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    chat = chat+' ' + message
    mess = {'role': 'user', 'content': message}
    messages.append(mess)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print(messages)
    print(chat)
    if completion.choices[0].message != None:
        # messages.append(dict(completion.choices[0].message))
        return completion.choices[0].message

    else:
        return 'Failed to Generate response!'


@app.route('/songs')
def my_form():
    return render_template('input.html')


@app.route("/songs", methods=['POST'])
def moodtape():
    pipe_lr, cv = joblib.load(
        open("Emotunes_nb_cv.pkl", "rb"))
    #chat = ['I am happy because i won a dance competition yesterday']
    mood = pipe_lr.predict(cv.transform([chat]))
    print(mood)
    username = request.form['username']
    token = util.prompt_for_user_token(username,
                                       scope=scope,
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri)
    spotify_auth = authenticate_spotify(token)
    top_artists = aggregate_top_artists(spotify_auth)

    top_tracks = aggregate_top_tracks(spotify_auth, top_artists)
    global selected_tracks
    selected_tracks = select_tracks(spotify_auth, top_tracks, mood)
    random.shuffle(selected_tracks)
    playlist_option = bool(request.form.get('create_playlist'))
    global playlist
    # Perform any action based on the create_playlist value
    if playlist_option:

        playlist = create_playlist(spotify_auth, selected_tracks, mood)
        print(playlist)
    else:
        playlist = None
    print('final', selected_tracks)
    return redirect(url_for('display_tracks', page=1))


@app.route('/songs/<int:page>')
def display_tracks(page):
    global playlist
    print(page)
    track_ids = selected_tracks  # Your list of track IDs
    tracks_per_page = 1  # Number of tracks to display per page
    start_index = (page - 1) * tracks_per_page
    end_index = start_index + tracks_per_page
    tracks = track_ids[start_index:end_index]
    print(tracks)
    return render_template('songs.html', track_ids=tracks, page=page, tracks_per_page=tracks_per_page, total=len(selected_tracks), playlist=playlist)
    # return render_template('songs.html', track_ids=selected_tracks[0:25])

@app.route("/profile", methods=["GET"])
def profile():
    chart_data={"labels":["sadness","joy"],"values":[1,1]}
    return render_template("profile.html", chart_data=chart_data)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
