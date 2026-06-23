Pythontify

I got tired of opening Spotify just to listen to music while coding, so I built this — a music player that lives entirely in the terminal. Arrow keys to browse, Enter to play. That's it.

Show Image
Show Image
Show Image


What it does


Scans your music folder and lists every .mp3 it finds
Arrow keys to navigate, Enter to play, S to stop
Progress bar that shows how far into a song you are
Music keeps playing while you scroll around the list
Autoplay — when a song ends it moves on to the next one and loops
Shuffle mode to mix things up



Preview

 PYTHONTIFY  [SHUFFLE]
 ▶  stairway_to_heaven.mp3  [########--------]  02:47 / 08:02
────────────────────────────────────────────────────────────────
     1. bohemian_rhapsody.mp3
     2. hotel_california.mp3
  ▶  3. stairway_to_heaven.mp3
     4. imagine.mp3
────────────────────────────────────────────────────────────────
  Now playing: stairway_to_heaven.mp3
 [↑↓] Move  [Enter] Play  [S] Stop  [X] Shuffle  [Q] Quit


Setup

You need Python 3.6+ (already on most Linux systems) and one of these audio players — Pythontify picks whichever one it finds first:

PlayerInstallmpg123sudo apt install mpg123mpvsudo apt install mpvvlcsudo apt install vlcffplaysudo apt install ffmpeg

For the progress bar to show actual song duration, also install ffmpeg:

bashsudo apt install ffmpeg


Running it

bashgit clone https://github.com/just-a-tech36/Pythontify.git
cd Pythontify
python3 "#Pythontify.py"

Before running, open #Pythontify.py and set MUSIC_DIR to wherever your music lives:

pythonMUSIC_DIR = "/your/music/folder"


Controls

KeyAction↑ / ↓Move through the listEnterPlay selected songSStopXToggle shuffleQQuit


How it's built

It uses Python's built-in curses module to draw the UI directly in the terminal. The screen refreshes every 500ms so the progress bar ticks forward without you having to press anything, and the music runs as a background process so the UI stays responsive while something's playing.

When a song finishes, it looks up the current track's position in the queue, moves to the next one, and starts it automatically. If shuffle is on, the queue is randomized — toggle it off and it resets back to alphabetical order.

No pip installs. No virtual environment. Everything except ffmpeg is standard library.


License

MIT — do whatever you want with it.
