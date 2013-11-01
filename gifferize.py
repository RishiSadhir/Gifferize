from flask import Flask, request, render_template
from base64 import b64encode
import requests
import string
import random
import re
import ConfigParser


app = Flask(__name__)


# Read config

config = ConfigParser.ConfigParser()
config.read("Gifferize.cfg")
API_KEY = config.get("Imgur", "client_id")
URL = "https://api.imgur/com/3/upload.json"
HEADERS = {"Authorization": "Client-ID " + API_KEY}
YT_USERNAME = config.get("YouTube", "username")
YT_PASS = config.get("YouTube", "password")

# Regex for youtube videos
yt_reg = re.compile("^(https://)?www.youtube.com/.*|(https://)?www.youtu.be/.*|(https://)m.youtube.com/*")


# Random string generator
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# Checks if YouTube link is valid
def is_valid_yt_link(link):
    yt_reg

# Uploads gif to imgur
def imgur_upload(path):
    rqst = requests.post(
        URL,
        headers=HEADERS,
        data={
            'key'   : API_KEY,
            "image" : b64encode(open(path, 'rb').read()),
            'type'  : 'base64',
            'name'  : path,
            'title' : path + " by Gifferize!"
        })
    return rqst.json()["data"]["link"]

# Render the homepaage
@app.route('/')
def welcome():
    return render_template("welcome.html")

# Render the about page
@app.route('/about')
def about():
    return render_template("about.html")

# upload that gif!
@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        link = request.form['link']
        start = request.form['start']
        end = request.form['end']

        return link + " " + start + " " + end
    else:
        return "error in post method!"



if __name__ == '__main__':
    app.run(debug=True)

