from dataclasses import dataclass
from typing import List, Optional
import mediapipe as mp
import cv2

@dataclass
class HandFrame:
    landmarks: List[tuple]   # [(x,y,z) normalized 0..1]
    handedness: str          # "Left" or "Right"
    score: float

class HandTracker:
    def __init__(self, max_hands=1, det_conf=0.6, track_conf=0.6):
        self._hands = mp.solutions.hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=det_conf,
            min_tracking_confidence=track_conf,
        )
        self._drawer = mp.solutions.drawing_utils
        self._styles = mp.solutions.drawing_styles

    def process(self, frame_bgr) -> Optional[List[HandFrame]]:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        res = self._hands.process(rgb)
        if not res.multi_hand_landmarks:
            return None
        out: List[HandFrame] = []
        for lm, hd in zip(res.multi_hand_landmarks, res.multi_handedness):
            pts = [(p.x, p.y, getattr(p, "z", 0.0)) for p in lm.landmark]
            out.append(HandFrame(pts, hd.classification[0].label, hd.classification[0].score))
        return out

    def draw(self, frame_bgr, hand_landmarks_list) -> None:
        if not hand_landmarks_list:
            return
        # We need original MP landmarks object to draw — so we redraw by coordinates (simpler: skip fancy styles)
        # Instead, just draw circles and lines between canonical connections:
        connections = mp.solutions.hands.HAND_CONNECTIONS
        h, w = frame_bgr.shape[:2]
        for hand in hand_landmarks_list:
            pts = [(int(x*w), int(y*h)) for (x,y,_) in hand.landmarks]
            # joints
            for (x,y) in pts:
                cv2.circle(frame_bgr, (x,y), 3, (0,255,0), -1)
            # bones
            for a,b in connections:
                ax,ay = pts[a]
                bx,by = pts[b]
                cv2.line(frame_bgr, (ax,ay), (bx,by), (0,200,0), 2)
