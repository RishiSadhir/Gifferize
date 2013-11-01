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

# Render the homepaage
@app.route('/')
def welcome():
    return render_template("welcome.html")

# Render the about page
@app.route('/about')
def about():
    return render_template("about.html")

# upload that gif
@app.route('/display', methods=['GET', 'POST'])
def display():
    # Gather post data
    if request.method == 'POST':
        link = request.form['link']
        start = request.form['start']
        end = request.form['end']

        if not yt_reg.match(link):
            return render_template("error.html", error="link",
                                   message="Looks like the link you gave me wasnt valid :(")
        if not verify_times(start, end):
            return render_template("error.html", error="time",
                                   message="I can't make gifs that long right now, try making it less than 15 seconds.")
        return youtube_to_gif(link, start, end)

    else:
        return render_template("error.html")


def youtube_to_gif(link, start, end):
    start, end, diffs = gather_times(start.strip(), end.strip())
    return "link: "+link+"\nstarts: " + start +"\nends: " + end

def verify_times(start, end):
    starts = [int(x.strip()) for x in start.split(":")[::-1]]
    ends = [int(x.strip()) for x in end.split(":")[::-1]]

    diff = []

    for i in range(0, len(starts)):
        diff.append(ends[i] - starts[i])

        if diff[i] < 0:
            ends[i+1] -= 1
            diff[i] += 60

        if diff[0] > 15:
            return False

        for i in range(1, len(diff)):
            if diff[i] > 0:
                return False
    return True
    

def gather_times(start, end):
    return start, end, end 

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


# Random string generator
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

if __name__ == '__main__':
    app.run(debug=True)
