from os.path import join, expanduser, exists
from json import load

formats = {
    "text": ["txt"],
    "image": ["png", "webp", "jpg", "jpeg"],
    "video": ["mp4", "mov", "m4a"],
    "sound": ["ogg", "mp3"]
}

keys = load(open(c)) if exists(c := join(expanduser("~"), "Code", "keys.json")) else {}

aliaFolder = join(expanduser("~"), "AppData", "Local", "Alia")

__all__ = ["formats", "keys", "aliaFolder"]
