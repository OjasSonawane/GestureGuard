import numpy as np

# MediaPipe landmark indices for hand
WRIST = 0
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20
INDEX_PIP = 6
INDEX_MCP = 5
MIDDLE_PIP = 10
MIDDLE_MCP = 9
RING_PIP = 14
RING_MCP = 13
PINKY_PIP = 18
PINKY_MCP = 17

def _angle(lm, i_tip, i_pip, i_mcp) -> float:
    v1 = np.array(lm[i_tip][:2]) - np.array(lm[i_pip][:2])
    v2 = np.array(lm[i_mcp][:2]) - np.array(lm[i_pip][:2])
    denom = (np.linalg.norm(v1)*np.linalg.norm(v2) + 1e-6)
    cosang = np.dot(v1, v2) / denom
    return float(np.degrees(np.arccos(np.clip(cosang, -1, 1))))

def finger_curls(lm):
    idx = _angle(lm, INDEX_TIP, INDEX_PIP, INDEX_MCP)
    mid = _angle(lm, MIDDLE_TIP, MIDDLE_PIP, MIDDLE_MCP)
    rin = _angle(lm, RING_TIP, RING_PIP, RING_MCP)
    lit = _angle(lm, PINKY_TIP, PINKY_PIP, PINKY_MCP)
    return idx, mid, rin, lit

def openness(lm) -> float:
    # average distance of finger tips from wrist
    tips = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
    w = np.array(lm[WRIST][:2])
    ds = [np.linalg.norm(np.array(lm[i][:2]) - w) for i in tips]
    return float(np.mean(ds))

def horizontal_direction(lm) -> float:
    # positive when index tip is to the RIGHT of wrist
    return float(lm[INDEX_TIP][0] - lm[WRIST][0])

def vertical_direction_thumb(lm) -> float:
    # positive when thumb tip is ABOVE wrist (remember y grows downward, so invert)
    return float(lm[WRIST][1] - lm[THUMB_TIP][1])
