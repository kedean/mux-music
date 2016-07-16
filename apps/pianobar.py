import subprocess
import timeout_decorator
import re

PIANOBAR_SESSION = "pianobar"
PIANOBAR_PIPE = "/home/pi/pianobar_pipe"

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

def pause():
    __sendKeys("S")

def resume():
    __sendKeys("P")

def next():
    __sendKeys("n")

@timeout_decorator.timeout(2, use_signals=False)
def __extractSongInfo():
    __ensurePipe()
    handle = open(PIANOBAR_PIPE, "r")
    __sendKeys("i")
    stationData = handle.readline()
    songData = handle.readline()   
    trackerData = handle.readline()
    handle.close()

    songInfo = re.search("\"(.*?)\" by \"(.*?)\" on \"(.*?)\"", songData).groups()
    return {"song":songInfo[0], "artist":songInfo[1], "album":songInfo[2]}

def songInfo():
    while True:
        try:
            return __extractSongInfo()
        except timeout_decorator.timeout_decorator.TimeoutError:
            print("Pipe timeout...retrying get operation...")



__init__()

actions = {"next":("POST", next), "pause":("POST", pause), "resume":("POST", resume), "songInfo":("GET", songInfo)}
