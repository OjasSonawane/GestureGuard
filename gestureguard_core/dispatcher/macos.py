import subprocess
from .base import ActionDispatcher

AS = "osascript"

def _osascript(script: str):
    subprocess.run([AS, "-e", script], check=False)

class MacOSDispatcher(ActionDispatcher):
    def play_pause(self):
        # Try Music app and Spotify
        _osascript('tell application "System Events" to key code 16 using {command down, option down}')
        # Fallback for Music
        _osascript('tell application "Music" to playpause')

    def next_track(self):
        _osascript('tell application "Music" to next track')
        _osascript('tell application "Spotify" to next track')

    def prev_track(self):
        _osascript('tell application "Music" to previous track')
        _osascript('tell application "Spotify" to previous track')

    def volume_up(self):
        _osascript('set o to output volume of (get volume settings)')
        _osascript('set volume output volume ((o + 6) min 100)')

    def volume_down(self):
        _osascript('set o to output volume of (get volume settings)')
        _osascript('set volume output volume ((o - 6) max 0)')

    def mute_toggle(self):
        _osascript('set m to output muted of (get volume settings)')
        _osascript('set volume output muted (not m)')
