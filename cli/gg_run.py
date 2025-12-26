import argparse, time, cv2
from gestureguard_core.camera import Camera
from gestureguard_core.hands import HandTracker
from gestureguard_core.gestures import detect_gesture
from gestureguard_core.config import load_config
from gestureguard_core.dispatcher import get_dispatcher

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--camera", type=int, default=None, help="Camera index override")
    ap.add_argument("--preview", action="store_true", help="Show preview window")
    args = ap.parse_args()

    cfg = load_config()
    cam_idx = args.camera if args.camera is not None else cfg.camera_index
    cam = Camera(index=cam_idx, size=(cfg.frame_width, cfg.frame_height), max_fps=cfg.max_fps)
    cam.open()
    tracker = HandTracker()
    disp = get_dispatcher()

    hold = 0
    cooldown = 0
    last_gesture = None

    try:
        while True:
            frame = cam.read()
            img = frame.bgr.copy()
            hands = tracker.process(img)
            gesture = None
            if hands and hands[0].score >= cfg.gestures.confidence_min:
                gesture = detect_gesture(hands[0].landmarks)

            if cooldown > 0:
                cooldown -= 1
            elif gesture is not None and cfg.enabled.get(gesture, True):
                if gesture == last_gesture:
                    hold += 1
                else:
                    last_gesture = gesture
                    hold = 1
                if hold >= cfg.gestures.hold_frames:
                    # fire action
                    if gesture == "open_palm": disp.play_pause()
                    elif gesture == "point_right": disp.next_track()
                    elif gesture == "point_left": disp.prev_track()
                    elif gesture == "thumb_up": disp.volume_up()
                    elif gesture == "thumb_down": disp.volume_down()
                    elif gesture == "fist": disp.mute_toggle()
                    cooldown = cfg.gestures.cooldown_frames
                    hold = 0
            else:
                hold = 0
                last_gesture = None

            if args.preview:
                # Draw simple text
                if gesture:
                    cv2.putText(img, f"{gesture}", (24, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)
                cv2.imshow("GestureGuard (CLI Preview)", img)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
    finally:
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
