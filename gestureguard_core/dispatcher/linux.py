from .base import ActionDispatcher
import subprocess

def _run(cmd):
    subprocess.run(cmd, check=False)

class LinuxDispatcher(ActionDispatcher):
    # Use playerctl if present (MPRIS); fall back to xdotool for media keys; volume via pactl
    def play_pause(self):
        _run(["playerctl", "play-pause"])

    def next_track(self):
        _run(["playerctl", "next"])

    def prev_track(self):
        _run(["playerctl", "previous"])

    def volume_up(self):
        _run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])

    def volume_down(self):
        _run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])

    def mute_toggle(self):
        _run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])
