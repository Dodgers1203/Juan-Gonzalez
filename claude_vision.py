import os
import json
import re
from groq import Groq

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    return _client

SYSTEM_PROMPT = """You are an elite Rocket League esports commentator like the casters at RLCS World Championship. You have deep knowledge of Rocket League mechanics and terminology.

When given a screenshot from a Rocket League match, respond ONLY with valid JSON with no extra text:
{
  "scene_label": "<one of: GOAL, Save, Aerial, Shot on Goal, Demolition, Overtime, Kickoff, Dribble, Boost Management, Rotation, Replay, Scoreboard, General Play>",
  "commentary": "<2-3 sentences of exciting accurate esports commentary using real RL terms>",
  "sentiment": "<one of: hype, tense, calm, analytical, dramatic>",
  "intensity": <number 1-10>,
  "game_state": "<score and time if visible, e.g. 2-1 Blue 1:23 remaining, or unknown>"
}"""


def analyze_frame(base64_image: str) -> dict:
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=400,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        },
                        {
                            "type": "text",
                            "text": "Analyze this Rocket League frame and generate commentary."
                        }
                    ]
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        print(f"[GROQ] Response: {raw[:100]}")
        result = json.loads(raw)
        return result

    except json.JSONDecodeError as e:
        print(f"[GROQ ERROR] JSON error: {e}")
        return {"scene_label": "General Play", "commentary": "The action continues!", "sentiment": "neutral", "intensity": 5, "game_state": "unknown"}
    except Exception as e:
        print(f"[GROQ ERROR] {e}")
        return {"scene_label": "General Play", "commentary": "The action continues!", "sentiment": "neutral", "intensity": 5, "game_state": "unknown"}
