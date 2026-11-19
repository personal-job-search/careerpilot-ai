import json
from pathlib import Path

PROFILE_PATH = Path("data/initial_profile.json")

def load_profile():
    if not PROFILE_PATH.exists():
        return {"name":"", "summary":"", "skills":{}, "experience":[]}
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

def save_profile(profile):
    PROFILE_PATH.parent.mkdir(exist_ok=True)
    PROFILE_PATH.write_text(json.dumps(profile, indent=2), encoding="utf-8")
