import threading
import os
import cv2
import streamlit as st

st.set_page_config(
    page_title="Narrador IA Rocket League",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #080c14 !important;
    color: #e2e8f0;
    font-family: 'Courier New', monospace;
}
.stApp { background-color: #080c14; }
h1 {
    background: linear-gradient(90deg, #f97316, #facc15);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.12em;
    font-size: 2rem !important;
}
h2, h3 { color: #f97316; letter-spacing: 0.08em; }
.stButton > button {
    background: linear-gradient(135deg, #f97316, #ea580c) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    box-shadow: 0 0 16px rgba(249,115,22,0.4) !important;
}
.rl-card {
    background: rgba(249,115,22,0.07);
    border: 1px solid rgba(249,115,22,0.3);
    border-left: 4px solid #f97316;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 8px 0;
    font-family: 'Courier New', monospace;
    line-height: 1.6;
}
.rl-card-goal     { background: rgba(250,204,21,0.12); border-left: 4px solid #facc15; box-shadow: 0 0 20px rgba(250,204,21,0.25); }
.rl-card-save     { background: rgba(34,197,94,0.10);  border-left: 4px solid #22c55e; }
.rl-card-aerial   { background: rgba(96,165,250,0.10); border-left: 4px solid #60a5fa; }
.rl-card-overtime { background: rgba(168,85,247,0.12); border-left: 4px solid #a855f7; }
.rl-card-demo     { background: rgba(239,68,68,0.10);  border-left: 4px solid #ef4444; }
.scene-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    margin-right: 8px;
    font-weight: 700;
}
.ts           { color: #475569; font-size: 0.68rem; }
.game-state   { color: #f97316; font-size: 0.70rem; margin-top: 2px; }
.commentary-t { color: #f1f5f9; font-size: 0.88rem; margin-top: 6px; }
.stProgress > div > div { background-color: #f97316 !important; }
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

BADGE_STYLE = {
    "GOAL":             "background:#facc15;color:#000;",
    "Save":             "background:#22c55e;color:#000;",
    "Aerial":           "background:#60a5fa;color:#000;",
    "Shot on Goal":     "background:#f97316;color:#000;",
    "Demolition":       "background:#ef4444;color:#fff;",
    "Overtime":         "background:#a855f7;color:#fff;",
    "Kickoff":          "background:#06b6d4;color:#000;",
    "Dribble":          "background:#84cc16;color:#000;",
    "Boost Management": "background:#f59e0b;color:#000;",
    "Rotation":         "background:#0ea5e9;color:#000;",
    "Replay":           "background:#475569;color:#fff;",
    "Scoreboard":       "background:#334155;color:#fff;",
    "General Play":     "background:#1e293b;color:#94a3b8;border:1px solid #334155;",
}

CARD_CLASS = {
    "GOAL":       "rl-card-goal",
    "Save":       "rl-card-save",
    "Aerial":     "rl-card-aerial",
    "Overtime":   "rl-card-overtime",
    "Demolition": "rl-card-demo",
}

SCENE_ICON = {
    "GOAL":             "⚽",
    "Save":             "🧤",
    "Aerial":           "✈️",
    "Shot on Goal":     "🎯",
    "Demolition":       "💥",
    "Overtime":         "⏱️",
    "Kickoff":          "🏁",
    "Dribble":          "🎱",
    "Boost Management": "⚡",
    "Rotation":         "🔄",
    "Replay":           "🎬",
    "Scoreboard":       "📊",
    "General Play":     "🚗",
}


def render_card(item: dict) -> str:
    label   = item["scene"]
    badge   = BADGE_STYLE.get(label, BADGE_STYLE["General Play"])
    extra   = CARD_CLASS.get(label, "")
    icon    = SCENE_ICON.get(label, "🎮")
    ts      = f"{item['timestamp']:.1f}s"
    diff    = f"Δ {item['diff']*100:.1f}%"
    gs      = item.get("game_state", "")
    gs_html = f'<div class="game-state">🏟 {gs}</div>' if gs and gs != "unknown" else ""

    return f"""
    <div class="rl-card {extra}">
        <span class="scene-badge" style="{badge}">{icon} {label}</span>
        <span class="ts">{ts} &nbsp;·&nbsp; {diff}</span>
        {gs_html}
        <div class="commentary-t">🎙 {item['commentary']}</div>
    </div>
    """


st.title("ROCKET LEAGUE AI NARRADOR")

col_left, col_right = st.columns([1.55, 1], gap="large")

with col_left:
    st.subheader("Clip de gameplay")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
    )

    video_file = st.file_uploader(
        "Rocket League .mp4 clip",
        type=["mp4", "mov", "avi"],
        label_visibility="collapsed",
    )

    if video_file:
        st.video(video_file)

    c1, c2 = st.columns(2)
    with c1:
        analysis_fps = st.slider("Sample rate (fps)", 1, 4, 2)
    with c2:
        threshold = st.slider("Scene sensitivity (%)", 1, 25, 7) / 100.0

    voice_on = st.toggle("Audio narrador", value=True)

with col_right:
    st.subheader("Commentario")
    feed_placeholder  = st.empty()
    metrics_row       = st.empty()
    frame_placeholder = st.empty()

st.markdown("<br>", unsafe_allow_html=True)
start_btn = st.button("▶ START COMMENTARY", use_container_width=True)

if start_btn:
    if not api_key:
        st.error("Ingresar llave Groq API")
        st.stop()
    if not video_file:
        st.error("Sube Rocket League clip")
        st.stop()

    os.environ["GROQ_API_KEY"] = api_key
    print(f"[DEBUG] Groq API key set: {api_key[:10]}...")

    from modules.capture       import extract_frames, frame_to_base64
    from modules.heuristic     import scene_changed
    from modules.claude_vision import analyze_frame
    from modules.tts           import speak

    with st.spinner("Extraer frames"):
        video_file.seek(0)
        frames = extract_frames(video_file, fps=analysis_fps)

    st.success(f"✅ {len(frames)} frames extracted — starting analysis…")

    progress_bar = st.progress(0.0)
    status_text  = st.empty()

    all_events = []
    prev_frame = None
    goals = saves = aerials = demos = 0

    for idx, (frame_idx, frame, timestamp) in enumerate(frames):
        progress_bar.progress((idx + 1) / len(frames))
        status_text.text(
            f"Analyzing frame {idx+1}/{len(frames)}  |  {len(all_events)} events…"
        )

        changed, diff_score, reason = scene_changed(prev_frame, frame, threshold)
        prev_frame = frame
        if not changed:
            continue

        b64    = frame_to_base64(frame)
        result = analyze_frame(b64)

        scene_label = result.get("scene_label", "General Play")
        commentary  = result.get("commentary", "")
        sentiment   = result.get("sentiment", "neutral")
        intensity   = result.get("intensity", 5)
        game_state  = result.get("game_state", "unknown")

        if voice_on and commentary:
            t = threading.Thread(target=speak, args=(commentary, sentiment), daemon=True)
            t.start()

        if scene_label == "GOAL":         goals   += 1
        elif scene_label == "Save":       saves   += 1
        elif scene_label == "Aerial":     aerials += 1
        elif scene_label == "Demolition": demos   += 1

        event = {
            "frame":      frame_idx,
            "timestamp":  timestamp,
            "scene":      scene_label,
            "commentary": commentary,
            "sentiment":  sentiment,
            "intensity":  intensity,
            "game_state": game_state,
            "diff":       diff_score,
            "reason":     reason,
        }
        all_events.append(event)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        with col_right:
            frame_placeholder.image(
                frame_rgb,
                caption=f"🔍 {scene_label} @ {timestamp:.1f}s",
                width=400,
            )

        with col_right:
            with metrics_row.container():
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Events",     len(all_events))
                m2.metric("⚽ Goals",   goals)
                m3.metric("🧤 Saves",   saves)
                m4.metric("✈️ Aerials", aerials)

        cards_html = "".join(render_card(e) for e in reversed(all_events[-20:]))
        with col_right:
            feed_placeholder.markdown(cards_html, unsafe_allow_html=True)

    progress_bar.progress(1.0)
    status_text.empty()
    st.balloons()
    st.success(
        f"🏁 Done! {len(all_events)} events · {goals} goals · "
        f"{saves} saves · {aerials} aerials · {demos} demos"
    )

    if all_events:
        import pandas as pd
        with st.expander("📊 Full Event Log"):
            df = pd.DataFrame(all_events)[
                ["timestamp", "scene", "intensity", "sentiment", "game_state", "commentary"]
            ]
            df.columns = ["Time(s)", "Scene", "Intensity", "Sentiment", "Game State", "Commentary"]
            df["Time(s)"] = df["Time(s)"].round(2)
            st.dataframe(df, use_container_width=True, hide_index=True)
