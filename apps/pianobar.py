import subprocess
import timeout_decorator
import re

PIANOBAR_SESSION = "pianobar"
PIANOBAR_PIPE = "/tmp/pianobar_pipe"
PIPE_TIMEOUT = 5

def __init__():
    main_session_exists = subprocess.Popen(["tmux", "has-session", "-t", PIANOBAR_SESSION])
    main_session_exists.wait()
    if main_session_exists.returncode != 0:
        p = subprocess.Popen(["tmux", "new-session", "-d", "-s", PIANOBAR_SESSION, "pianobar"])
        p.wait()

def __sendKeys(*args):
    keys = list(args)
    p = subprocess.Popen(["tmux", "send-keys", "-t", PIANOBAR_SESSION] + keys)
    p.wait()

def __ensurePipe():
    subprocess.Popen(["mkfifo", PIANOBAR_PIPE]).wait() #doesn't matter if it passes, as long as there's a pipe afterwards
    #TODO: check if there is now a new pipe
    p = subprocess.Popen(["tmux", "pipe-pane", "-t", PIANOBAR_SESSION + ".0", "-o", "tee " + PIANOBAR_PIPE]) #tells tmux to send everything through 'tee' into a named pipe, this avoids corrupting the stdout
    p.wait()

"""
Calls the given function and returns back the data, looping and trying again if the initial call takes too long.
"""
def __getPipedFunction(func):
    """
    Note: Unfortunately, the pipe only works ~90% of the time.
    To work around this, we set a timeout that only allows the piping to run for a set amount of time. 
    If it takes too long, that means the other end of the pipe never opened, so we just try again!
    """
    while True:
        try:
            return func()
        except timeout_decorator.timeout_decorator.TimeoutError:
            print("Pipe timeout...retrying get operation...")

def pause():
    __sendKeys("S")

def resume():
    __sendKeys("P")

def next():
    __sendKeys("n")

@timeout_decorator.timeout(PIPE_TIMEOUT, use_signals=False)
def __extractSongInfo():
    __ensurePipe()
    handle = open(PIANOBAR_PIPE, "r")
    __sendKeys("i")
    stationData = handle.readline()
    songData = handle.readline()   
    trackerData = handle.readline()
    print(trackerData)
    handle.close()
    return (stationData, songData, trackerData)

"""
Fetches information about the current song
"""
def songInfo():
    stationData, songData, trackerData = __getPipedFunction(__extractSongInfo)
    songInfo = re.search("\"(.*?)\" by \"(.*?)\" on \"(.*?)\"", songData).groups()
    trackInfo = re.search("#\s+-(\d+:\d+)\/(\d+:\d+)", trackerData).groups()
    return {"song":songInfo[0], "artist":songInfo[1], "album":songInfo[2], "remaining":trackInfo[0], "duration":trackInfo[1]}

def duration():
    info = songInfo()
    return {"remaining":info["remaining"], "duration":info["duration"]}

"""
Fetches raw station information as a list of lines
"""
@timeout_decorator.timeout(PIPE_TIMEOUT, use_signals=False)
def __extractStations():
    __ensurePipe()
    handle = open(PIANOBAR_PIPE, "r")
    __sendKeys("s", "Enter")
    stationLines = []
    while True:
        line = handle.readline()
        if "[?] Select station:" in line:
            break
        else:
            stationLines.append(line.strip())
    handle.close()
    return stationLines

def stations():
    lines = __getPipedFunction(__extractStations)
    
    # once we have the station data, get the info out of it. The info consists of an id for switching, the name of the station, and whether or not its part of quickmix (indicated by a 'q' in the string)
    station_matcher = re.compile("(\\d+)\\)\\s*(q?)\\s+(.*?)$")
    matches = [station_matcher.search(line) for line in lines]
    output = [{"id":match.group(1), "is_quickmix":(match.group(2) == "q"), "name":match.group(3)} for match in matches]
    return output

def getCurrentStation():
    stationData, songData, trackerData = __getPipedFunction(__extractSongInfo)
    stationName = re.search("Station \"(.*?)\" \(\d+\)", stationData)
    return {"station":stationName.group(1)}

def setCurrentStation(id):
    __sendKeys("s", id, "Enter")

__init__()
actions = {
"next":{"POST":next}, 
"pause":{"POST":pause},
"resume":{"POST":resume},
"songInfo":{"GET":songInfo},
"duration":{"GET":duration},
"stations":{"GET":stations},
"currentStation":{
    "GET":getCurrentStation,
    "POST":setCurrentStation
}
}
