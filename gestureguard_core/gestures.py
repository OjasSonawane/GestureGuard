from typing import Literal, Optional
from .features import finger_curls, openness, horizontal_direction, vertical_direction_thumb

GestureName = Literal["open_palm", "fist", "point_left", "point_right", "thumb_up", "thumb_down"]

def detect_gesture(lm) -> Optional[GestureName]:
    idx, mid, rin, lit = finger_curls(lm)
    open_score = (idx + mid + rin + lit) / 4.0
    open_palm = open_score < 35
    fist = open_score > 60

    horiz = horizontal_direction(lm)
    thumb_v = vertical_direction_thumb(lm)

    # Pointing: index extended (low curl) + horizontal displacement
    point_right = (idx < 30 and mid > 50 and rin > 50 and lit > 50 and horiz > 0.04)
    point_left  = (idx < 30 and mid > 50 and rin > 50 and lit > 50 and horiz < -0.04)

    thumb_up = (thumb_v > 0.03 and mid > 50 and rin > 50 and lit > 50)
    thumb_down = (thumb_v < -0.03 and mid > 50 and rin > 50 and lit > 50)

    if open_palm: return "open_palm"
    if fist: return "fist"
    if point_right: return "point_right"
    if point_left: return "point_left"
    if thumb_up: return "thumb_up"
    if thumb_down: return "thumb_down"
    return None
