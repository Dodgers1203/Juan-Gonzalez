"""
capture.py — Extract frames from a video file.
"""
import cv2
import tempfile
import os
import base64


def extract_frames(video_source, fps: int = 2):
    """
    Extract frames at the requested sample rate.
    Returns list of (frame_index, bgr_ndarray, timestamp_seconds).
    """
    tmp_path = None
    if hasattr(video_source, "read"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(video_source.read())
            tmp_path = tmp.name
        path = tmp_path
    else:
        path = video_source

    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {path}")

    native_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    interval   = max(1, int(native_fps / fps))
    frames     = []
    i          = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i % interval == 0:
            frames.append((i, frame, i / native_fps))
        i += 1

    cap.release()
    if tmp_path and os.path.exists(tmp_path):
        os.unlink(tmp_path)

    return frames


def frame_to_base64(frame_bgr) -> str:
    """Convert a BGR numpy frame to a base64 JPEG string for the API."""
    import cv2
    _, buffer = cv2.imencode(".jpg", frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 75])
    return base64.b64encode(buffer).decode("utf-8")


def get_video_info(video_source):
    """Return basic video metadata."""
    if hasattr(video_source, "read"):
        video_source.seek(0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(video_source.read())
            tmp_path = tmp.name
        video_source.seek(0)
    else:
        tmp_path = video_source

    cap = cv2.VideoCapture(tmp_path)
    info = {
        "fps":      cap.get(cv2.CAP_PROP_FPS),
        "frames":   int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "duration": cap.get(cv2.CAP_PROP_FRAME_COUNT) / max(1, cap.get(cv2.CAP_PROP_FPS)),
        "width":    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height":   int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    cap.release()
    if hasattr(video_source, "read") and os.path.exists(tmp_path):
        os.unlink(tmp_path)
    return info
