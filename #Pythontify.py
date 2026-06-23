#Pythontify
import os
import glob
import curses
import subprocess
import sys
import time
import random
 
MUSIC_DIR = "/your/music/folder"
 
def get_mp3_files(directory):
    pattern = os.path.join(directory, "**", "*.mp3")
    files = glob.glob(pattern, recursive=True)
    files += glob.glob(os.path.join(directory, "*.mp3"))
    seen = set()
    unique = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return sorted(unique)
 
def play_song(filepath):
    players = ["mpg123", "mpv", "vlc", "ffplay", "mplayer"]
    for player in players:
        if subprocess.run(["which", player], capture_output=True).returncode == 0:
            if player == "vlc":
                return subprocess.Popen([player, "--intf", "dummy", filepath],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif player == "ffplay":
                return subprocess.Popen([player, "-nodisp", "-autoexit", filepath],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                return subprocess.Popen([player, filepath],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return None
 
def get_duration(filepath):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filepath],
        capture_output=True, text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0
 
def fmt_time(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"
 
def draw_ui(stdscr, songs, selected, now_playing, status_msg, play_start, song_duration, shuffled):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
 
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK,   curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_BLACK,   curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_CYAN,    -1)
    curses.init_pair(4, curses.COLOR_YELLOW,  -1)
    curses.init_pair(5, curses.COLOR_WHITE,   -1)
    curses.init_pair(6, curses.COLOR_GREEN,   -1)
    curses.init_pair(7, curses.COLOR_MAGENTA, -1)
    curses.init_pair(8, curses.COLOR_BLACK,   curses.COLOR_MAGENTA)
 
    shuffle_tag = " SHUFFLE " if shuffled else ""
    title = " PYTHONTIFY "
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(0, 0, title.ljust(w)[:w])
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
    if shuffled:
        stdscr.attron(curses.color_pair(8) | curses.A_BOLD)
        stdscr.addstr(0, len(title), shuffle_tag[:w - len(title)])
        stdscr.attroff(curses.color_pair(8) | curses.A_BOLD)
 
    if now_playing is not None:
        name = os.path.basename(songs[now_playing])
        elapsed = time.time() - play_start if play_start else 0
        elapsed = min(elapsed, song_duration)
        time_str = f" {fmt_time(elapsed)} / {fmt_time(song_duration)} "
        bar_width = max(w - len(name) - len(time_str) - 8, 4)
        filled = int((elapsed / song_duration) * bar_width) if song_duration > 0 else 0
        bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
        now_line = f" \u25b6  {name}  {bar}{time_str}"
        stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(1, 0, now_line[:w].ljust(w)[:w])
        stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
    else:
        stdscr.attron(curses.color_pair(5))
        stdscr.addstr(1, 0, " \u25a0  Nothing is playing".ljust(w)[:w])
        stdscr.attroff(curses.color_pair(5))
 
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(2, 0, ("\u2500" * (w - 1))[:w - 1])
    stdscr.attroff(curses.color_pair(4))
 
    list_start = 3
    list_end = h - 3
    visible = list_end - list_start
 
    if len(songs) == 0:
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(list_start + 1, 0, f"  No .mp3 files found in: {MUSIC_DIR}"[:w])
        stdscr.attroff(curses.color_pair(4))
    else:
        offset = max(0, selected - visible // 2)
        offset = min(offset, max(0, len(songs) - visible))
 
        for i, idx in enumerate(range(offset, min(offset + visible, len(songs)))):
            row = list_start + i
            name = os.path.basename(songs[idx])
            num = f"{idx + 1:>3}."
            if idx == now_playing:
                indicator = " \u25b6 "
            else:
                indicator = "   "
            line = f" {indicator} {num} {name}"
 
            if idx == selected:
                stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                stdscr.addstr(row, 0, line[:w - 1].ljust(w - 1))
                stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
            elif idx == now_playing:
                stdscr.attron(curses.color_pair(6) | curses.A_BOLD)
                stdscr.addstr(row, 0, line[:w - 1])
                stdscr.attroff(curses.color_pair(6) | curses.A_BOLD)
            else:
                stdscr.attron(curses.color_pair(5))
                stdscr.addstr(row, 0, line[:w - 1])
                stdscr.attroff(curses.color_pair(5))
 
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(h - 3, 0, ("\u2500" * (w - 1))[:w - 1])
    stdscr.attroff(curses.color_pair(4))
 
    if status_msg:
        stdscr.attron(curses.color_pair(7))
        stdscr.addstr(h - 2, 0, f"  {status_msg}"[:w])
        stdscr.attroff(curses.color_pair(7))
 
    controls = " [\u2191\u2193] Move  [Enter] Play  [S] Stop  [X] Shuffle  [Q] Quit "
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.insstr(h - 1, 0, controls[:w - 1].ljust(w - 1))
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
 
    stdscr.refresh()
 
def playlist(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.timeout(500)
 
    songs = get_mp3_files(MUSIC_DIR)
    queue = list(range(len(songs)))
    shuffled = False
    selected = 0
    now_playing = None
    player_proc = None
    play_start = None
    song_duration = 0
    status_msg = f"Found {len(songs)} songs" if songs else "No songs found!"
 
    while True:
        if player_proc and player_proc.poll() is not None:
            player_proc = None
            play_start = None
            song_duration = 0
            if now_playing is not None:
                pos = queue.index(now_playing)
                next_pos = (pos + 1) % len(queue)
                next_idx = queue[next_pos]
                proc = play_song(songs[next_idx])
                if proc:
                    player_proc = proc
                    now_playing = next_idx
                    selected = next_idx
                    play_start = time.time()
                    song_duration = get_duration(songs[next_idx])
                    status_msg = f"Now playing: {os.path.basename(songs[next_idx])}"
                else:
                    now_playing = None
                    status_msg = "Playback finished."
            else:
                status_msg = "Playback finished."
 
        draw_ui(stdscr, songs, selected, now_playing, status_msg, play_start, song_duration, shuffled)
        key = stdscr.getch()
 
        if key == curses.KEY_UP:
            if songs:
                selected = (selected - 1) % len(songs)
                status_msg = ""
 
        elif key == curses.KEY_DOWN:
            if songs:
                selected = (selected + 1) % len(songs)
                status_msg = ""
 
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            if songs:
                if player_proc:
                    player_proc.terminate()
                    player_proc = None
                proc = play_song(songs[selected])
                if proc:
                    player_proc = proc
                    now_playing = selected
                    play_start = time.time()
                    song_duration = get_duration(songs[selected])
                    status_msg = f"Now playing: {os.path.basename(songs[selected])}"
                else:
                    status_msg = "Error: No player found (install mpg123, mpv, or vlc)"
 
        elif key in (ord("s"), ord("S")):
            if player_proc:
                player_proc.terminate()
                player_proc = None
                now_playing = None
                play_start = None
                song_duration = 0
                status_msg = "Stopped."
 
        elif key in (ord("x"), ord("X")):
            shuffled = not shuffled
            if shuffled:
                random.shuffle(queue)
                status_msg = "Shuffle ON"
            else:
                queue = list(range(len(songs)))
                status_msg = "Shuffle OFF"
 
        elif key in (ord("q"), ord("Q")):
            if player_proc:
                player_proc.terminate()
            break
 
if __name__ == "__main__":
    if not os.path.isdir(MUSIC_DIR):
        print(f"Error: Directory '{MUSIC_DIR}' does not exist.")
        sys.exit(1)
    curses.wrapper(playlist)
 