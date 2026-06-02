import subprocess
import queue
import threading

_speech_queue = queue.Queue()
_worker_started = False


def _speech_worker():
    while True:
        try:
            text, sentiment = _speech_queue.get(timeout=30)
            print(f"[TTS] Speaking: {text[:50]}")
            safe_text = text.replace('"', "'").replace("\\", "")
            subprocess.run(
                ["say", "-v", "Alex", "-r", "150", safe_text],
                check=False
            )
            _speech_queue.task_done()
        except queue.Empty:
            continue


def speak(text: str, sentiment: str = "neutral") -> None:
    global _worker_started
    print(f"[TTS] speak() called with: {text[:50]}")

    if not text or not text.strip():
        return

    if not _worker_started:
        t = threading.Thread(target=_speech_worker, daemon=True)
        t.start()
        _worker_started = True

    while not _speech_queue.empty():
        try:
            _speech_queue.get_nowait()
            _speech_queue.task_done()
        except queue.Empty:
            break

    _speech_queue.put((text, sentiment))
