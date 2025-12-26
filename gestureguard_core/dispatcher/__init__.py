from .base import ActionDispatcher
from ..utils import current_os
from .windows import WindowsDispatcher
from .macos import MacOSDispatcher
from .linux import LinuxDispatcher

def get_dispatcher() -> ActionDispatcher:
    osname = current_os()
    if osname == "windows":
        return WindowsDispatcher()
    if osname == "macos":
        return MacOSDispatcher()
    return LinuxDispatcher()
