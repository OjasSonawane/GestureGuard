import time
from dataclasses import dataclass
from typing import Optional, Tuple
import cv2

@dataclass
class Frame:
    bgr: any
    timestamp: float

class Camera:
    def __init__(self, index: int = 0, size: Tuple[int, int] = (960, 540), max_fps: int = 30):
        self.index = index
        self.size = size
        self.max_fps = max_fps
        self.cap: Optional[cv2.VideoCapture] = None

    def open(self):
        self.cap = cv2.VideoCapture(self.index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Camera {self.index} could not be opened")
        w, h = self.size
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        self.cap.set(cv2.CAP_PROP_FPS, self.max_fps)

    def read(self) -> Frame:
        assert self.cap is not None, "Camera not opened"
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Failed to read from camera")
        return Frame(frame, time.time())

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
