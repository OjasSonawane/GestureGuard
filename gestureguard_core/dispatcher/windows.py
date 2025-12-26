# Minimal Windows backend using keyboard + pycaw (if available)
import time
import ctypes
from .base import ActionDispatcher

# Virtual-Key codes for media keys
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
APPCOMMAND_VOLUME_MUTE = 0x80000
APPCOMMAND_VOLUME_UP = 0x0a0000
APPCOMMAND_VOLUME_DOWN = 0x090000

HWND_BROADCAST = 0xFFFF
WM_APPCOMMAND = 0x0319

def _press_vk(vk):
    ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.01)
    ctypes.windll.user32.keybd_event(vk, 0, 2, 0)

def _app_command(cmd):
    ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_APPCOMMAND, 0, cmd)

class WindowsDispatcher(ActionDispatcher):
    def play_pause(self): _press_vk(VK_MEDIA_PLAY_PAUSE)
    def next_track(self): _press_vk(VK_MEDIA_NEXT_TRACK)
    def prev_track(self): _press_vk(VK_MEDIA_PREV_TRACK)
    def volume_up(self): _app_command(APPCOMMAND_VOLUME_UP)
    def volume_down(self): _app_command(APPCOMMAND_VOLUME_DOWN)
    def mute_toggle(self): _app_command(APPCOMMAND_VOLUME_MUTE)
