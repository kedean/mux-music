#!/usr/bin/python3

import apps.pianobar as pianobar
import json
from flask import Flask

mux = Flask(__name__)

#
# Handles all requests for now
# In the future this will become a delegator that determines what apps have been loaded and dispatches dynamically
#
@mux.route("/<app>/<action>")
def handleAll(app, action):
    status = 200
    
    if app == "pianobar":    
        if action == "pause":
            pianobar.pause()
        elif action == "resume":
            pianobar.resume()
        elif action == "next":
            pianobar.next()
        else:
            status = 404 
    else:
        status = 404

    return json.dumps({"status":status, "app":app, "action":action})

if __name__ == "__main__":
    mux.run(host="0.0.0.0", port=8000)
