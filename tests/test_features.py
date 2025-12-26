import numpy as np
from gestureguard_core.features import finger_curls

def test_finger_curls_shape():
    # 21 fake landmarks
    lm = [(0.0,0.0,0.0)] * 21
    vals = finger_curls(lm)
    assert len(vals) == 4
