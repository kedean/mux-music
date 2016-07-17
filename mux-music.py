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
        function_by_method = pianobar.actions.get(action)
        if function_by_method is None:
            abort(404) 
        else:
            function = function_by_method.get(request.method)
            if function is None:
                abort(405)
            else:
                response["status"] = 200
                response["payload"] = function()
    else:
        abort(404)
    return json.dumps(response)

if __name__ == "__main__":
    mux.run(host="0.0.0.0", port=8000)
