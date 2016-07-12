#!/usr/bin/python3

import apps.pianobar as pianobar
import json
from flask import Flask

mux = Flask(__name__)

@mux.route("/")
def hello():
    return "Hello World!"

@mux.route("/<app>/<action>")
def pause(app, action):
    status = 200
    
    if action == "pause":
        pianobar.pause()
    elif action == "resume":
        pianobar.resume()
    elif action == "next":
        pianobar.next()
    else:
        status = 404 

    return json.dumps({"status":status, "action":action})    

if __name__ == "__main__":
    mux.run(host="0.0.0.0", port=8000)
