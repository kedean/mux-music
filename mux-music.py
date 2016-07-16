#!/usr/bin/python3

import apps.pianobar as pianobar
import json
from flask import Flask
from flask import request
from flask import abort

mux = Flask(__name__)

#
# Handles all requests for now
#
@mux.route("/v1/<app>/<action>")
def handleAll(app, action):
    response = {}
    
    if app == "pianobar":
        method = pianobar.actions.get(action)
        if method is None:
            abort(404) 
        elif method[0] != request.method:
            abort(405) 
        else:
            response["status"] = 200
            response["payload"] = method[1]()
    else:
        abort(404)
    return json.dumps(response)

if __name__ == "__main__":
    mux.run(host="0.0.0.0", port=8000)
