import subprocess

PIANOBAR_SESSION = "pianobar"

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

def pause():
    __sendKeys("S")

def resume():
    __sendKeys("P")

def next():
    __sendKeys("n")

__init__()
