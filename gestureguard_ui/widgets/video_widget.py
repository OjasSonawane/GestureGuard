from PySide6.QtCore import Qt, QMutex, QMutexLocker, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel

import cv2

class VideoWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self._mutex = QMutex()
        self._frame = None

    def update_frame(self, frame_bgr):
        with QMutexLocker(self._mutex):
            self._frame = frame_bgr

    def paintEvent(self, event):
        with QMutexLocker(self._mutex):
            if self._frame is not None:
                rgb = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
                self.setPixmap(QPixmap.fromImage(img).scaled(self.width(), self.height(), Qt.KeepAspectRatio))
        super().paintEvent(event)
