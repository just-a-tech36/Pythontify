# Pythontify

I got tired of opening Spotify just to listen to music while coding, so I built this — a music player that lives entirely in the terminal. Arrow keys to browse, Enter to play. That's it.

![Python](https://img.shields.io/badge/Python-3.6+-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux-orange?logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What it does

- Scans your music folder and lists every `.mp3` it finds
- Arrow keys to navigate, Enter to play, S to stop
- Progress bar that shows how far into a song you are
- Music keeps playing while you scroll around the list
- Simple sign-up screen before you get in (email + code)

---

## Preview

```
 MUSIC PLAYLIST
 >> bohemian_rhapsody.mp3  [########--------]  01:23 / 05:54
--------------------------------------------------------------
     1. bohemian_rhapsody.mp3
     2. hotel_california.mp3
  >> 3. stairway_to_heaven.mp3
     4. imagine.mp3
--------------------------------------------------------------
  Now playing: stairway_to_heaven.mp3
 [Up/Down] Navigate  [Enter] Play  [S] Stop  [Q] Quit
```

---

## Setup

You need Python 3.6+ (already on most Linux systems) and one of these audio players:

| Player | Install |
|--------|---------|
| `mpg123` | `sudo apt install mpg123` |
| `mpv` | `sudo apt install mpv` |
| `vlc` | `sudo apt install vlc` |
| `ffplay` | `sudo apt install ffmpeg` |

Pythontify just picks whichever one you already have. If you want the progress bar to show the actual song duration, also install ffmpeg:

```bash
sudo apt install ffmpeg
```

---

## Running it

```bash
git clone https://github.com/yourusername/pythontify.git
cd pythontify
python3 music_app.py
```

It'll ask for a Gmail address and a verification code. Use `3667` as the code.

By default it looks for music in `/home/elliot/Music`. To point it somewhere else, change this line near the top of `music_app.py`:

```python
MUSIC_DIR = "/your/music/folder"
```

---

## Controls

| Key | Action |
|-----|--------|
| `↑` / `↓` | Move through the list |
| `Enter` | Play selected song |
| `S` | Stop |
| `Q` | Quit |

---

## How it's built

Two stages, back to back.

First is the sign-up flow — plain terminal input, nothing fancy. Once you're through, it hands off to the main player.

The player uses Python's `curses` module to draw and update the UI directly in the terminal. The screen refreshes every 500ms so the progress bar moves smoothly, and the music runs as a background process so the UI never freezes while something's playing.

No external dependencies outside of `ffmpeg` for reading song length. Everything else is standard library.

---

## License

MIT — do whatever you want with it.
