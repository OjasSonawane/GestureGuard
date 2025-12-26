import sys, threading, time, cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QSlider
from gestureguard_core.camera import Camera
from gestureguard_core.hands import HandTracker
from gestureguard_core.gestures import detect_gesture
from gestureguard_core.config import load_config, save_config
from gestureguard_core.dispatcher import get_dispatcher
from .widgets.video_widget import VideoWidget

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GestureGuard")
        self.cfg = load_config()
        self.cam = Camera(self.cfg.camera_index, (self.cfg.frame_width, self.cfg.frame_height), self.cfg.max_fps)
        self.tracker = HandTracker()
        self.disp = get_dispatcher()

        self.video = VideoWidget(self)
        self.status = QLabel("Status: Idle")
        self.camera_select = QComboBox()
        for i in range(5):
            self.camera_select.addItem(f"Camera {i}", i)
        self.camera_select.setCurrentIndex(self.cfg.camera_index)

        self.sensitivity = QSlider(Qt.Horizontal)
        self.sensitivity.setMinimum(3); self.sensitivity.setMaximum(15)
        self.sensitivity.setValue(self.cfg.gestures.hold_frames)

        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop"); self.stop_btn.setEnabled(False)

        top = QHBoxLayout()
        top.addWidget(QLabel("Camera:"))
        top.addWidget(self.camera_select)
        top.addWidget(QLabel("Hold frames:"))
        top.addWidget(self.sensitivity)
        top.addStretch()
        top.addWidget(self.start_btn)
        top.addWidget(self.stop_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.video)
        layout.addWidget(self.status)

        self._running = False
        self._thread = None
        self._hold = 0
        self._cooldown = 0
        self._last = None

        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)
        self.sensitivity.valueChanged.connect(self.update_hold_frames)
        self.camera_select.currentIndexChanged.connect(self.change_camera)

        self._ui_timer = QTimer(self)
        self._ui_timer.timeout.connect(self.refresh_status)
        self._ui_timer.start(200)

    def change_camera(self, idx):
        self.cfg.camera_index = idx
        save_config(self.cfg)

    def update_hold_frames(self, v):
        self.cfg.gestures.hold_frames = int(v)
        save_config(self.cfg)

    def refresh_status(self):
        running = "Running" if self._running else "Idle"
        self.status.setText(f"Status: {running}")

    def loop(self):
        self.cam.open()
        self._running = True
        try:
            while self._running:
                f = self.cam.read()
                img = f.bgr
                hands = self.tracker.process(img)
                gesture = None
                if hands and hands[0].score >= self.cfg.gestures.confidence_min:
                    gesture = detect_gesture(hands[0].landmarks)

                if self._cooldown > 0:
                    self._cooldown -= 1
                elif gesture is not None and self.cfg.enabled.get(gesture, True):
                    if gesture == self._last:
                        self._hold += 1
                    else:
                        self._last = gesture
                        self._hold = 1
                    if self._hold >= self.cfg.gestures.hold_frames:
                        if gesture == "open_palm": self.disp.play_pause()
                        elif gesture == "point_right": self.disp.next_track()
                        elif gesture == "point_left": self.disp.prev_track()
                        elif gesture == "thumb_up": self.disp.volume_up()
                        elif gesture == "thumb_down": self.disp.volume_down()
                        elif gesture == "fist": self.disp.mute_toggle()
                        self._cooldown = self.cfg.gestures.cooldown_frames
                        self._hold = 0
                else:
                    self._hold = 0
                    self._last = None

                self.video.update_frame(img)
                self.video.update()
                
        finally:
            self.cam.release()

    def start(self):
        if self._running: return
        self._thread = threading.Thread(target=self.loop, daemon=True)
        self._thread.start()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop(self):
        self._running = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    w = App()
    w.resize(1000, 700)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
