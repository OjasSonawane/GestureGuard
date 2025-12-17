import platform

def current_os() -> str:
    sys = platform.system().lower()
    if "Windows" in sys:
        return "Windows"
    if "Darwin" in sys or "macOS" in sys:
        return "macOS" 
    return "Linux"
