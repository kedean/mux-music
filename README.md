# mux-music
Locally hosted music controller API

## Installing dependencies (on Debian)
`sudo apt-get install python3 tmux pianobar pip3`
`sudo pip3 install timeout-decorator flask`

## Configuring
Only pianobar must be configured beforehand. Follow the below guide to configure pianobar to automatically log in on start.

https://wiki.archlinux.org/index.php/Pianobar

## Running
By default, mux-music runs on port 8000 and is visible to the outside world. Run it with `python3 mux-music.py` from the downlod directory. *Python 2 will not work.* Once the server has declared that it is running, you may access it from any browser that can reach the host. Test it by going to http://HOST_IP:8000/v1/pianobar/songInfo

## Available actions
Currently only the pianobar app is supported. Available POST actions are 'next', 'pause', and 'resume'. The only available GET action is 'songInfo'. These will be expanded on later.

The API is versioned. Access by http://HOST_IP:PORT_NO/v1/APP/ACTION 
