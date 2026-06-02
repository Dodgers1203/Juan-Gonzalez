"""
heuristic.py — Only send frames to Claude when the scene actually changed.
Saves API calls and makes commentary feel event-driven.
"""
import cv2
import numpy as np


def scene_changed(prev_frame, curr_frame, threshold: float = 0.07):
    """
    Returns (changed: bool, diff_score: float, reason: str).
    """
    if prev_frame is None:
        return True, 1.0, "first_frame"

    prev_gray = cv2.cvtColor(cv2.resize(prev_frame, (160, 90)), cv2.COLOR_BGR2GRAY).astype(float)
    curr_gray = cv2.cvtColor(cv2.resize(curr_frame, (160, 90)), cv2.COLOR_BGR2GRAY).astype(float)
    full_diff = float(np.abs(prev_gray - curr_gray).mean() / 255.0)

    # Check scoreboard region (top center) for goal events
    h, w = prev_frame.shape[:2]
    prev_score = prev_frame[0:int(h*0.08), int(w*0.35):int(w*0.65)]
    curr_score = curr_frame[0:int(h*0.08), int(w*0.35):int(w*0.65)]
    pg = cv2.cvtColor(cv2.resize(prev_score, (80, 20)), cv2.COLOR_BGR2GRAY).astype(float)
    cg = cv2.cvtColor(cv2.resize(curr_score, (80, 20)), cv2.COLOR_BGR2GRAY).astype(float)
    score_diff = float(np.abs(pg - cg).mean() / 255.0)

    if full_diff > 0.40:
        return True, full_diff, "replay_or_cut"
    if score_diff > 0.15:
        return True, score_diff, "score_changed"
    if full_diff > threshold:
        return True, full_diff, "motion"

    return False, full_diff, "no_change"
